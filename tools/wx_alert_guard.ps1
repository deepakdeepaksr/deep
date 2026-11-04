<#
.SYNOPSIS
    KiCad "wxWidgets Debug Alert" auto-dismiss guard.

.DESCRIPTION
    KiCad 10.0 (build-win-10.0-stable) ships with wxWidgets assertions enabled.
    Certain PCB edits hit e.g. pcb/pcb_track.cpp(387): assert 'false' failed in
    'GetWidth'  ->  "PCB_VIA::GetWidth called without a layer argument", and
    wxMSW pops a modal "wxWidgets Debug Alert" dialog (Yes / No / Cancel).

    That dialog is raised from inside KiCad's own event loop, so it cannot be
    disabled from a KiCad preference, config file or environment variable -
    the only supported way out is the dialog's own [Cancel] button, which tells
    wxWidgets to suppress further warnings for the rest of the session.

    This script is a tiny background watchdog that waits for that dialog and
    clicks [Cancel] on KiCad's behalf, so the alert never interrupts work.

.USAGE
    powershell -NoProfile -ExecutionPolicy Bypass -File wx_alert_guard.ps1                  # run the watchdog
    powershell -NoProfile -ExecutionPolicy Bypass -File wx_alert_guard.ps1 -Once             # one-shot sweep
    powershell -NoProfile -ExecutionPolicy Bypass -File wx_alert_guard.ps1 -Status        # is a guard alive?
    powershell -NoProfile -ExecutionPolicy Bypass -File wx_alert_guard.ps1 -Stop           # kill the guard
    powershell -NoProfile -ExecutionPolicy Bypass -File wx_alert_guard.ps1 -Pause          # leave alerts alone
    powershell -NoProfile -ExecutionPolicy Bypass -File wx_alert_guard.ps1 -Resume         # auto-cancel again
    powershell -NoProfile -ExecutionPolicy Bypass -File wx_alert_guard.ps1 -SelfTest       # fake dialog + dismiss
    powershell -NoProfile -ExecutionPolicy Bypass -File wx_alert_guard.ps1 -FakeAlert 20000  # show a stand-in alert and
                                                 # probe it: proves the installed guard closes it

.NOTES
    Author    : project tooling
    Requires  : Windows PowerShell 5.1 or PowerShell 7.x, no external modules
    Log file  : %LOCALAPPDATA%\KiCadWxAlertGuard\guard.log
#>
[CmdletBinding()]
param(
    [int]    $IntervalMs = 400,
    [int]    $FakeAlert = 0,
    [int]    $ProbeAfter = 3000,
    [switch] $Once,
    [switch] $Stop,
    [switch] $Pause,
    [switch] $Resume,
    [switch] $Status,
    [switch] $SelfTest
)

Set-StrictMode -Version 2
$ErrorActionPreference = 'Stop'

$taskName   = 'KiCadWxAlertGuard'
$logDir     = Join-Path $env:LOCALAPPDATA 'KiCadWxAlertGuard'
$logFile    = Join-Path $logDir 'guard.log'
$mutexName  = 'Local\KiCadWxAlertGuard.SingleInstance'
$alertTitle = 'wxWidgets Debug Alert'
$pauseFile  = Join-Path $logDir 'paused'

function Write-GuardLog {
    param([string]$Message)
    try {
        if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir -Force | Out-Null }
        # keep the log from growing without bound
        if ((Test-Path $logFile) -and ((Get-Item $logFile).Length -gt 262144)) {
            Get-Content $logFile -Tail 100 | Set-Content $logFile -Encoding UTF8
        }
        "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')  $Message" | Add-Content -Path $logFile -Encoding UTF8
    } catch { }
}

# ---------------------------------------------------------------- Win32 layer
$native = @'
using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.Text;

namespace KiCadWxGuard
{
    public static class Native
    {
        public delegate bool EnumProc(IntPtr hWnd, IntPtr lParam);

        [DllImport("user32.dll")]  public static extern bool EnumWindows(EnumProc cb, IntPtr l);
        [DllImport("user32.dll")]  public static extern bool EnumChildWindows(IntPtr p, EnumProc cb, IntPtr l);
        [DllImport("user32.dll", CharSet = CharSet.Unicode)]
        public static extern int GetWindowTextW(IntPtr h, StringBuilder s, int max);
        [DllImport("user32.dll", CharSet = CharSet.Unicode)]
        public static extern int GetClassNameW(IntPtr h, StringBuilder s, int max);
        [DllImport("user32.dll")]  public static extern bool IsWindowVisible(IntPtr h);
        [DllImport("user32.dll")]  public static extern bool IsWindow(IntPtr h);
        [DllImport("user32.dll")]  public static extern uint GetWindowThreadProcessId(IntPtr h, out uint pid);
        [DllImport("user32.dll")]  public static extern IntPtr GetParent(IntPtr h);
        [DllImport("user32.dll")]  public static extern int GetDlgCtrlID(IntPtr h);
        [DllImport("user32.dll")]  public static extern IntPtr GetWindow(IntPtr h, uint cmd);
        [DllImport("user32.dll")]  public static extern IntPtr PostMessageW(IntPtr h, uint msg, IntPtr w, IntPtr l);
        [DllImport("user32.dll")]  public static extern IntPtr SendMessageW(IntPtr h, uint msg, IntPtr w, IntPtr l);
        [DllImport("user32.dll")]  public static extern bool SetForegroundWindow(IntPtr h);
        [DllImport("user32.dll")]  public static extern bool BringWindowToTop(IntPtr h);

        [StructLayout(LayoutKind.Sequential)]
        public struct FLASHWINFO
        {
            public uint cbSize; public IntPtr hwnd; public uint dwFlags; public uint uCount; public uint dwTimeout;
        }
        [DllImport("user32.dll")] public static extern bool FlashWindowEx(ref FLASHWINFO pfwi);

        public const uint WM_KEYDOWN       = 0x0100;
        public const uint WM_KEYUP         = 0x0101;
        public const uint WM_COMMAND       = 0x0111;
        public const uint BM_CLICK         = 0x00F5;
        public const uint BM_SETCHECK      = 0x00F1;
        public const uint VK_ESCAPE        = 0x1B;
        public const uint BN_CLICKED       = 0;
        public const uint GW_OWNER         = 4;
        public const uint FLASHW_ALL       = 3;
        public const uint FLASHW_TIMERNOFG = 12;

        public static string Text(IntPtr h)
        {
            var sb = new StringBuilder(512);
            try { GetWindowTextW(h, sb, sb.Capacity); } catch { }
            return sb.ToString();
        }

        public static string Class(IntPtr h)
        {
            var sb = new StringBuilder(256);
            try { GetClassNameW(h, sb, sb.Capacity); } catch { }
            return sb.ToString();
        }

        /// <summary>All visible top-level windows whose title matches <paramref name="title"/> (case-insensitive).</summary>
        public static List<IntPtr> FindWindows(string title)
        {
            var found = new List<IntPtr>();
            EnumWindows(delegate(IntPtr h, IntPtr l)
            {
                if (!IsWindowVisible(h)) return true;
                string t = Text(h);
                if (t.Length > 0 && t.IndexOf(title, StringComparison.OrdinalIgnoreCase) >= 0) found.Add(h);
                return true;
            }, IntPtr.Zero);
            return found;
        }

        /// <summary>Direct children of <paramref name="parent"/> that are buttons with the given caption.</summary>
        public static List<IntPtr> FindButtons(IntPtr parent, string caption)
        {
            var found = new List<IntPtr>();
            EnumChildWindows(parent, delegate(IntPtr h, IntPtr l)
            {
                string cls = Class(h);
                if (cls.IndexOf("Button", StringComparison.OrdinalIgnoreCase) < 0) return true;
                string t = Text(h).Trim();
                if (t.Length > 0 && t.IndexOf(caption, StringComparison.OrdinalIgnoreCase) >= 0) found.Add(h);
                return true;
            }, IntPtr.Zero);
            return found;
        }

        /// <summary>Every button caption inside a dialog (for diagnostics).</summary>
        public static List<string> ButtonCaptions(IntPtr parent)
        {
            var list = new List<string>();
            EnumChildWindows(parent, delegate(IntPtr h, IntPtr l)
            {
                if (Class(h).IndexOf("Button", StringComparison.OrdinalIgnoreCase) >= 0)
                {
                    string t = Text(h).Trim();
                    if (t.Length > 0) list.Add(t);
                }
                return true;
            }, IntPtr.Zero);
            return list;
        }

        public static uint PidOf(IntPtr h)
        {
            uint pid;
            try { GetWindowThreadProcessId(h, out pid); } catch { pid = 0; }
            return pid;
        }

        /// <summary>Level 1: a real click on the button control.</summary>
        public static bool ClickButton(IntPtr button)
        {
            if (!IsWindow(button)) return false;
            try { BringWindowToTop(GetParent(button)); } catch { }
            try { SetForegroundWindow(GetParent(button)); } catch { }
            try { PostMessageW(button, BM_CLICK, IntPtr.Zero, IntPtr.Zero); return true; } catch { return false; }
        }

        /// <summary>Level 2: WM_COMMAND/BN_CLICKED straight to the parent dialog.</summary>
        public static bool SendCommand(IntPtr dialog, IntPtr button)
        {
            try
            {
                int id = GetDlgCtrlID(button);
                IntPtr wParam = new IntPtr((id << 16) | (int)BN_CLICKED);
                PostMessageW(dialog, WM_COMMAND, wParam, button);
                return true;
            }
            catch { return false; }
        }

        /// <summary>Level 3: Escape keystroke, which maps to the dialog's Cancel default.</summary>
        public static bool SendEscape(IntPtr dialog)
        {
            try
            {
                IntPtr esc = new IntPtr((int)VK_ESCAPE);
                PostMessageW(dialog, WM_KEYDOWN, esc, IntPtr.Zero);
                PostMessageW(dialog, WM_KEYUP, esc, IntPtr.Zero);
                return true;
            }
            catch { return false; }
        }

        /// <summary>Level 4: hard close, last resort so KiCad is never left frozen.</summary>
        public static bool CloseWindow(IntPtr dialog)
        {
            try { PostMessageW(dialog, 0x0010 /*WM_CLOSE*/, IntPtr.Zero, IntPtr.Zero); return true; }
            catch { return false; }
        }

        public static void Flash(IntPtr h)
        {
            try
            {
                var fi = new FLASHWINFO();
                fi.cbSize = (uint)Marshal.SizeOf(typeof(FLASHWINFO));
                fi.hwnd = h; fi.dwFlags = FLASHW_ALL | FLASHW_TIMERNOFG; fi.uCount = 3; fi.dwTimeout = 0;
                FlashWindowEx(ref fi);
            }
            catch { }
        }
    }
}
'@

if (-not ('KiCadWxGuard.Native' -as [type])) {
    Add-Type -TypeDefinition $native -Language CSharp -ErrorAction Stop
}
$Native = [KiCadWxGuard.Native]

# C# stand-in for the wx alert window - only used by -SelfTest / -FakeAlert.
$testerCode = @'
using System;
using System.Threading;
using System.Windows.Forms;

namespace KiCadWxGuard
{
    public static class Tester
    {
        public static string LastClicked = "";
        public static int OpenedCount = 0;

        public static void ShowFakeAlert(int ms)
        {
            var t = new Thread(delegate()
            {
                LastClicked = "";
                var f = new Form();
                f.Text = "wxWidgets Debug Alert";
                f.FormBorderStyle = FormBorderStyle.FixedDialog;
                f.StartPosition = FormStartPosition.CenterScreen;
                f.ClientSize = new System.Drawing.Size(520, 150);
                var lbl = new Label();
                lbl.Text = "assert 'false' failed in GetWidth\n(self-test only)";
                lbl.AutoSize = false;
                lbl.SetBounds(12, 12, 496, 60);
                var yes = new Button(); yes.Text = "Yes";    yes.SetBounds(220, 95, 80, 26);
                var no  = new Button(); no.Text  = "No";     no.SetBounds(305, 95, 80, 26);
                var cancel = new Button(); cancel.Text = "Cancel"; cancel.SetBounds(390, 95, 80, 26);
                yes.DialogResult = DialogResult.Yes;
                no.DialogResult  = DialogResult.No;
                cancel.DialogResult = DialogResult.Cancel;
                // A native modal dialog closes as soon as any button is clicked; a modeless
                // WinForms form does not, so emulate the real behaviour for a faithful test.
                yes.Click    += delegate { LastClicked = "Yes";    f.Close(); };
                no.Click     += delegate { LastClicked = "No";     f.Close(); };
                cancel.Click += delegate { LastClicked = "Cancel"; f.Close(); };
                f.Controls.Add(lbl); f.Controls.Add(yes); f.Controls.Add(no); f.Controls.Add(cancel);
                f.CancelButton = cancel;
                f.Show();
                OpenedCount = OpenedCount + 1;
                var deadline = DateTime.Now.AddMilliseconds(ms);
                while (DateTime.Now < deadline && f.Visible)
                {
                    Application.DoEvents();
                    Thread.Sleep(30);
                }
                f.Close();
                Application.DoEvents();
            });
            t.IsBackground = true;
            t.SetApartmentState(ApartmentState.STA);
            t.Start();
        }
    }
}
'@

function Ensure-TesterType {
    if ('KiCadWxGuard.Tester' -as [type]) { return $true }
    try {
        Add-Type -TypeDefinition $testerCode -Language CSharp -ReferencedAssemblies 'System.Windows.Forms','System.Drawing' -ErrorAction Stop
        return $true
    } catch {
        Write-Host "  stand-in alert UI is unavailable here: $($_.Exception.Message)" -ForegroundColor Yellow
        Write-Host '  (harmless - the watchdog itself only needs user32)'
        return $false
    }
}

# ------------------------------------------------------------- guard plumbing
function Get-GuardProcesses {
    <#
        Finds other watchdog instances. Two traps to avoid:
          * "install_wx_alert_guard.ps1" contains "wx_alert_guard.ps1" as a substring,
            so the installer must be filtered out explicitly;
          * utility switches (-Status/-Stop/...) run in a process that is not a watchdog.
        Ancestors are skipped too, so a launcher/wrapper never counts as a second guard.
    #>
    $exclude = @($PID)
    try {
        $cur = [int]$PID
        for ($i = 0; $i -lt 12 -and $cur -gt 0; $i++) {
            $p = Get-CimInstance Win32_Process -Filter "ProcessId=$cur" -ErrorAction SilentlyContinue
            if (-not $p) { break }
            $cur = [int]$p.ParentProcessId
            if ($cur -gt 0 -and ($exclude -notcontains $cur)) { $exclude += $cur }
        }
    } catch { }

    try {
        Get-CimInstance Win32_Process -Filter "Name='powershell.exe' OR Name='pwsh.exe'" -ErrorAction Stop |
            Where-Object {
                ($exclude -notcontains [int]$_.ProcessId) -and
                ($_.CommandLine -match '(?<!install_)wx_alert_guard\.ps1') -and
                ($_.CommandLine -notmatch 'install_wx_alert_guard') -and
                ($_.CommandLine -notmatch '\-(Status|Stop|SelfTest|Once|FakeAlert)')
            } |
            ForEach-Object { Get-Process -Id $_.ProcessId -ErrorAction SilentlyContinue }
    } catch { @() }
}

function Stop-Guard {
    $procs = @(Get-GuardProcesses)
    if ($procs.Count -eq 0) { Write-Host 'No KiCadWxAlertGuard process is running.'; return }
    $procs | ForEach-Object {
        Write-Host "Stopping guard PID $($_.Id)"
        try { $_.Kill(); $_.WaitForExit(5000) | Out-Null } catch { }
    }
    Write-GuardLog 'guard stopped by -Stop'
}

function Show-Status {
    $procs = @(Get-GuardProcesses)
    if ($procs.Count -gt 0) {
        Write-Host ("GUARD RUNNING  - PID(s): " + (($procs | ForEach-Object { $_.Id }) -join ', '))
    } else {
        Write-Host 'GUARD NOT RUNNING'
    }
    $tn = 'KiCadWxAlertGuard'
    try {
        $t = Get-ScheduledTask -TaskName $tn -ErrorAction SilentlyContinue
        if ($t) { Write-Host ("SCHEDULED TASK : {0} ({1})" -f $t.TaskName, $t.State) }
        else { Write-Host 'SCHEDULED TASK : not registered' }
    } catch { Write-Host 'SCHEDULED TASK : unavailable' }
    if (Test-Path $logFile) {
        Write-Host "LOG              : $logFile"
        Get-Content $logFile -Tail 8 | ForEach-Object { Write-Host "  $_" }
    }
}

function Invoke-DismissalSweep {
    <#
        Looks for the wx alert dialog and dismisses it via [Cancel].
        Returns $true when at least one dialog was handled in this pass.
    #>
    # Kill switch: while the pause flag exists the alert is left alone, so assertions
    # can actually be read when debugging KiCad itself.
    if (Test-Path $pauseFile) { return $false }

    $handled = $false
    $dialogs = $Native::FindWindows($alertTitle)
    if ($dialogs.Count -eq 0) { return $false }

    foreach ($dlg in $dialogs) {
        if (-not $Native::IsWindow($dlg)) { continue }

        $procId   = $Native::PidOf($dlg)
        $pname = ''
        try { $pname = (Get-Process -Id $procId -ErrorAction SilentlyContinue).ProcessName } catch { }

        $btns = @($Native::FindButtons($dlg, 'Cancel'))
        if ($btns.Count -eq 0) { $btns = @($Native::FindButtons($dlg, 'Abort')) }   # wx locale variants
        if ($btns.Count -eq 0) { $btns = @($Native::FindButtons($dlg, 'Cancelar')) }

        $captions = ($Native::ButtonCaptions($dlg)) -join ' | '
        Write-GuardLog ("alert dialog seen  win=0x{0:X} pid={1} proc={2} buttons=[{3}]" -f [long]$dlg.ToInt64(), $procId, $pname, $captions)

        if ($btns.Count -gt 0) {
            $btn = $btns[0]
            $Native::ClickButton($btn) | Out-Null
        } else {
            # No named Cancel button (localised build?) - Escape == Cancel on a Win32 dialog.
            $Native::SendEscape($dlg) | Out-Null
        }

        # Escalate only if the dialog is still up after the click had time to land.
        foreach ($wait in 250, 500, 900) {
            Start-Sleep -Milliseconds $wait
            if (-not $Native::IsWindow($dlg)) { break }
        }
        if ($Native::IsWindow($dlg)) {
            Write-GuardLog '  BM_CLICK did not close it -> WM_COMMAND BN_CLICKED'
            if ($btns.Count -gt 0) { $Native::SendCommand($dlg, $btns[0]) | Out-Null }
            else { $Native::SendEscape($dlg) | Out-Null }
            Start-Sleep -Milliseconds 600
        }
        if ($Native::IsWindow($dlg)) {
            Write-GuardLog '  WM_COMMAND did not close it -> Escape'
            $Native::SendEscape($dlg) | Out-Null
            Start-Sleep -Milliseconds 600
        }
        if ($Native::IsWindow($dlg)) {
            Write-GuardLog '  Escape did not close it -> WM_CLOSE (KiCad left unblocked)'
            $Native::CloseWindow($dlg) | Out-Null
        }

        Start-Sleep -Milliseconds 150
        if ($Native::IsWindow($dlg)) {
            Write-GuardLog '  WARNING: dialog still present after all dismissal levels'
        } else {
            Write-GuardLog '  dismissed (further wx warnings are now suppressed for this KiCad session)'
        }
        $handled = $true
    }
    return $handled
}

function Test-FakeAlertHost {
    <#
        -FakeAlert <ms> : show the stand-in "wxWidgets Debug Alert", probe it after
        -ProbeAfter ms, then clean up. This process never dismisses anything itself, so
        "still open" proves no watchdog is watching and "closed within" proves the
        installed background guard did the cancelling.
    #>
    param([int]$Ms, [int]$ProbeAfter = 3000)
    if (-not (Ensure-TesterType)) { return $false }
    [KiCadWxGuard.Tester]::ShowFakeAlert($Ms)

    # The stand-in is built on a background STA thread - wait until it is really on screen
    # before timing anything, otherwise "closed in 0.01s" just means "never appeared".
    $appeared = $false
    for ($i = 0; $i -lt 80; $i++) {
        if ($Native::FindWindows($alertTitle).Count -gt 0) { $appeared = $true; break }
        Start-Sleep -Milliseconds 100
    }
    if (-not $appeared) {
        Write-Host '  FAIL: the stand-in window never appeared on screen' -ForegroundColor Red
        return $false
    }

    $sw = [System.Diagnostics.Stopwatch]::StartNew()
    $closedAt = -1.0
    while ($sw.ElapsedMilliseconds -lt $ProbeAfter) {
        if ($Native::FindWindows($alertTitle).Count -eq 0) { $closedAt = $sw.Elapsed.TotalSeconds; break }
        Start-Sleep -Milliseconds 100
    }

    if ($closedAt -ge 0) {
        Write-Host ("  closed within {0:N2}s - dismissed by the background guard" -f $closedAt)
        return $false          # did NOT survive
    }

    $live = @($Native::FindWindows($alertTitle))
    if ($live.Count -gt 0) {
        Write-Host ("  still open after {0}ms - nothing dismissed it" -f $ProbeAfter)
        $Native::CloseWindow($live[0]) | Out-Null   # don't leave our own test window behind
        return $true           # survived
    }
    Write-Host '  test window vanished before it could be probed - inconclusive'
    return $false
}

function Start-SelfTest {
    Write-Host 'Building a stand-in "wxWidgets Debug Alert" dialog to prove the guard works...'
    if (-not (Ensure-TesterType)) { return }

    # 60 s lifetime: if the window vanishes in ~1 s it was the guard, not a timeout.
    [KiCadWxGuard.Tester]::ShowFakeAlert(60000)
    Write-Host '  a stand-in "wxWidgets Debug Alert" window is on screen - the guard will close it...'

    $appeared = $false
    for ($i = 0; $i -lt 20; $i++) {
        Start-Sleep -Milliseconds 250
        if ($Native::FindWindows($alertTitle).Count -gt 0) { $appeared = $true; break }
    }
    if (-not $appeared) {
        Write-Host '  FAIL: the stand-in window was never detected by the guard' -ForegroundColor Red
        return
    }

    $sw = [System.Diagnostics.Stopwatch]::StartNew()
    $liveGuard = @(Get-GuardProcesses).Count -gt 0
    if ($liveGuard) {
        Write-Host '  a background guard process is running - letting IT close the window...'
    } else {
        Write-Host '  no background guard running - exercising the in-process dismissal path...'
        Invoke-DismissalSweep | Out-Null
    }

    $gone = $false
    for ($i = 0; $i -lt 40; $i++) {
        if (-not ($Native::FindWindows($alertTitle).Count -gt 0)) { $gone = $true; break }
        Start-Sleep -Milliseconds 250
    }
    $sw.Stop()

    if (-not $gone) {
        Write-Host '  FAIL: stand-in window survived the dismissal ladder' -ForegroundColor Red
        return
    }
    $clicked = [KiCadWxGuard.Tester]::LastClicked
    Write-Host ("  closed in {0:N2}s via the [{1}] button" -f $sw.Elapsed.TotalSeconds, $clicked)
    if ($clicked -eq 'Cancel') {
        Write-Host '  OK - the guard presses exactly the same button you would press by hand' -ForegroundColor Green
    } else {
        Write-Host "  WARNING: expected the [Cancel] button, recorded [$clicked]" -ForegroundColor Yellow
    }
}

# ------------------------------------------------------------------------ run
if ($Status) { Show-Status; return }
if ($Stop)   { Stop-Guard;   return }
if ($Pause) {
    if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir -Force | Out-Null }
    Set-Content -Path $pauseFile -Value (Get-Date -Format 'o') -Encoding ASCII
    Write-GuardLog 'guard PAUSED - alerts will stay on screen until -Resume'
    Write-Host "Alert guard paused. KiCad will show the wxWidgets Debug Alert normally."
    Write-Host ("Resume with:  powershell -File ""$PSCommandPath"" -Resume")
    return
}
if ($Resume) {
    Remove-Item $pauseFile -Force -ErrorAction SilentlyContinue
    Write-GuardLog 'guard RESUMED'
    Write-Host 'Alert guard resumed - alerts are auto-cancelled again.'
    return
}
if ($SelfTest) { Start-SelfTest; return }
if ($FakeAlert -gt 0) { Test-FakeAlertHost -Ms $FakeAlert -ProbeAfter $ProbeAfter | Out-Null; return }

if ($Once) {
    # one-shot sweep, e.g. from a KiCad launch wrapper - no watchdog, no single-instance claim
    if (Invoke-DismissalSweep) { Write-Host 'wx alert dismissed.' } else { Write-Host 'no wx alert present.' }
    return
}

if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir -Force | Out-Null }

# Single instance. A named mutex alone is not enough: a "Local\" object namespace is
# per logon session, so an elevated / other-session launch would slip through. Scan for
# a peer guard process first, then take the mutex as a second layer.
$peers = @(Get-GuardProcesses)
if ($peers.Count -gt 0) {
    Write-GuardLog (("another guard is already running (PID {0}) - this instance exits" -f (($peers | ForEach-Object { $_.Id }) -join ',')))
    Write-Host 'A KiCadWxAlertGuard is already running - nothing to do.'
    return
}

$mutex = $null
try { $mutex = New-Object System.Threading.Mutex($false, "Global\$taskName") } catch { $mutex = $null }
if (-not $mutex) { try { $mutex = New-Object System.Threading.Mutex($false, $mutexName) } catch { $mutex = $null } }
if ($mutex -and -not $mutex.WaitOne(0, $false)) {
    Write-GuardLog 'another guard instance is already running - exiting'
    $mutex.Dispose()
    return
}

try {
    Write-GuardLog ("guard started  pid={0} ps={1} interval={2}ms" -f $PID, $PSVersionTable.PSVersion.ToString(), $IntervalMs)

    # Continuous watchdog: cheap title-match poll, only touches Win32 when the alert exists.
    while ($true) {
        try { Invoke-DismissalSweep | Out-Null }
        catch { Write-GuardLog ("sweep error: $($_.Exception.Message)") }
        try { Start-Sleep -Milliseconds $IntervalMs }
        catch { Start-Sleep -Milliseconds $IntervalMs }   # never let a sleep hiccup kill the guard
    }
} catch {
    Write-GuardLog ("guard aborted: $($_.Exception.Message)")
    throw
} finally {
    if ($mutex) { try { $mutex.ReleaseMutex() } catch { }; $mutex.Dispose() }
    Write-GuardLog 'guard exiting'
}
