<#
.SYNOPSIS
    Installs / removes the KiCad "wxWidgets Debug Alert" auto-dismiss guard so that
    pressing [Cancel] on the alert becomes permanent default behaviour on this PC.

.DESCRIPTION
    Registers wx_alert_guard.ps1 so it starts automatically at logon and stays running
    in the background. Whenever KiCad pops the modal wxWidgets assertion dialog, the
    guard clicks its [Cancel] button, which also tells wxWidgets to stop reporting
    further warnings for that KiCad session.

    Primary mechanism : Windows Scheduled Task  "KiCadWxAlertGuard"  (AtLogOn, hidden).
    Fallback mechanism: a hidden launcher in the per-user Startup folder
                        (%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup), used
                        automatically if task registration is blocked by policy.

.USAGE
    install_wx_alert_guard.ps1              # install + start now
    install_wx_alert_guard.ps1 -Status      # show what is installed
    install_wx_alert_guard.ps1 -Uninstall   # remove task, startup entry and process
    install_wx_alert_guard.ps1 -StartupFolderOnly   # skip Task Scheduler, use Startup folder

.NOTES
    Runs per-user, no administrator rights required for either mechanism.
#>
[CmdletBinding()]
param(
    [switch] $Uninstall,
    [switch] $Status,
    [switch] $StartupFolderOnly
)

$ErrorActionPreference = 'Stop'

$taskName   = 'KiCadWxAlertGuard'
$toolsDir   = $PSScriptRoot
$guardScript = Join-Path $toolsDir 'wx_alert_guard.ps1'
$startupDir  = Join-Path $env:APPDATA 'Microsoft\Windows\Start Menu\Programs\Startup'
$launcherVbs = Join-Path $toolsDir 'wx_alert_guard_launcher.vbs'
$logDir      = Join-Path $env:LOCALAPPDATA 'KiCadWxAlertGuard'

# Windows PowerShell 5.1 is present on every Windows build and needs no extra runtime.
$psExe = Join-Path $env:Windir 'System32\WindowsPowerShell\v1.0\powershell.exe'
if (-not (Test-Path $psExe)) {
    $psExe = (Get-Command pwsh.exe -ErrorAction SilentlyContinue).Source
}
if (-not $psExe) { throw 'No PowerShell host found (powershell.exe / pwsh.exe).' }

function Write-Step { param([string]$m) Write-Host "  $m" }
function Write-Ok   { param([string]$m) Write-Host "  $m" -ForegroundColor Green }
function Write-Warn { param([string]$m) Write-Host "  $m" -ForegroundColor Yellow }

function Get-HostState {
    $state = [pscustomobject]@{
        Task       = $null
        TaskInfo   = $null
        StartupLnk = (Test-Path (Join-Path $startupDir 'KiCadWxAlertGuard.lnk'))
        Vbs        = (Test-Path $launcherVbs)
        Running    = @()
    }
    try {
        $t = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
        if ($t) { $state.Task = $t.State; $state.TaskInfo = $t }
    } catch { }
    try {
        # NB: 'install_wx_alert_guard.ps1' contains 'wx_alert_guard.ps1' as a substring, and the
        # -Status/-Stop/... helper runs are not watchdog instances - both must be filtered out.
        $mine = $PID
        $state.Running = @(Get-CimInstance Win32_Process -Filter "Name='powershell.exe' OR Name='pwsh.exe'" -ErrorAction SilentlyContinue |
            Where-Object {
                $_.ProcessId -ne $mine -and
                ($_.CommandLine -match '(?<!install_)wx_alert_guard\.ps1') -and
                ($_.CommandLine -notmatch 'install_wx_alert_guard') -and
                ($_.CommandLine -notmatch '\-(Status|Stop|SelfTest|Once|FakeAlert)')
            })
    } catch { }
    return $state
}

function Stop-RunningGuard {
    $st = Get-HostState
    foreach ($p in $st.Running) {
        try { Stop-Process -Id $p.ProcessId -Force -ErrorAction SilentlyContinue; Write-Step "stopped guard process PID $($p.ProcessId)" } catch { }
    }
}

function Show-Status {
    Write-Host "KiCad wxWidgets alert guard - status"
    Write-Host "  guard script   : $guardScript"
    $st = Get-HostState
    Write-Host ("  scheduled task : " + $(if ($null -ne $st.Task) { "$($st.Task)" } else { 'not registered' }))
    Write-Host ("  startup entry  : " + $(if ($st.StartupLnk) { 'installed' } else { 'not installed' }))
    Write-Host ("  process        : " + $(if ($st.Running.Count -gt 0) { "running (PID $(($st.Running | ForEach-Object { $_.ProcessId }) -join ', '))" } else { 'not running' }))
    if (Test-Path (Join-Path $logDir 'guard.log')) {
        Write-Host "  recent log ($((Join-Path $logDir 'guard.log'))):"
        Get-Content (Join-Path $logDir 'guard.log') -Tail 10 | ForEach-Object { Write-Host "    $_" }
    }
}

function Remove-Install {
    Write-Host 'Uninstalling KiCad wxWidgets alert guard...'
    Stop-RunningGuard
    try {
        if (Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue) {
            Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
            Write-Ok 'scheduled task removed'
        } else { Write-Step 'scheduled task not present' }
    } catch { Write-Warn "could not remove scheduled task: $($_.Exception.Message)" }

    $lnk = Join-Path $startupDir "$taskName.lnk"
    if (Test-Path $lnk) { Remove-Item $lnk -Force; Write-Ok "removed $lnk" }
    if (Test-Path $launcherVbs) { Remove-Item $launcherVbs -Force; Write-Ok "removed $launcherVbs" }
    Write-Ok 'done - KiCad will show the alert normally again'
}

function ConvertTo-VbsLiteral {
    param([string]$Text)
    # VBScript string literal: wrap in " and double every embedded " - no hand-written
    # """" soup, which is easy to get wrong by exactly one quote and then fails silently.
    $q = [string][char]34
    return $q + $Text.Replace($q, $q + $q) + $q
}

function New-HiddenLauncher {
    # A .vbs wrapper lets the Startup folder start PowerShell with zero console flash.
    $q        = [string][char]34
    $cmdLine  = $q + $psExe + $q + ' -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File ' + $q + $guardScript + $q
    $lines = @(
        "' Starts the KiCad wxWidgets Debug Alert guard with no visible window.",
        'Option Explicit',
        'Dim shell, cmd',
        'Set shell = CreateObject("WScript.Shell")',
        ('cmd = ' + (ConvertTo-VbsLiteral $cmdLine)),
        'shell.Run cmd, 0, false'
    )
    # WScript wants plain text with CRLF line endings.
    $enc = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($launcherVbs, (($lines -join "`r`n") + "`r`n"), $enc)

    # Verify what was actually written, so a malformed launcher can never ship silently.
    $written = Get-Content $launcherVbs -Raw
    foreach ($line in ($written -split "`r`n")) {
        if (([regex]::Matches($line, [regex]::Escape($q)).Count % 2) -ne 0) {
            throw "generated launcher has an unbalanced quote on this line:`n  $line"
        }
    }
    Write-Step "created hidden launcher $launcherVbs"
}

function Install-StartupFolder {
    New-HiddenLauncher
    if (-not (Test-Path $startupDir)) { New-Item -ItemType Directory -Path $startupDir -Force | Out-Null }
    $lnk = Join-Path $startupDir "$taskName.lnk"
    try {
        $sh = New-Object -ComObject WScript.Shell
        $sc = $sh.CreateShortcut($lnk)
        $sc.TargetPath = "$env:SystemRoot\System32\wscript.exe"
        $sc.Arguments  = """$launcherVbs"""
        $sc.WorkingDirectory = $toolsDir
        $sc.Description = 'Auto-dismiss the KiCad wxWidgets Debug Alert'
        $sc.Save()
        Write-Ok "Startup-folder entry installed -> $lnk"
        return $true
    } catch {
        Write-Warn "could not create the Startup shortcut: $($_.Exception.Message)"
        return $false
    }
}

function Install-ScheduledTask {
    $argLine = "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$guardScript`""
    try {
        $action  = New-ScheduledTaskAction -Execute $psExe -Argument $argLine
        $trigger = New-ScheduledTaskTrigger -AtLogOn
        $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
                    -StartWhenAvailable -MultipleInstances IgnoreNew -RestartInterval (New-TimeSpan -Minutes 5) `
                    -RestartCount 3 -ExecutionTimeLimit (New-TimeSpan -Seconds 0)

        $principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive -RunLevel Limited

        Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings `
            -Principal $principal -Description 'Silently clicks Cancel on the KiCad wxWidgets Debug Alert dialog so it never blocks the PCB editor.' -Force | Out-Null
        Write-Ok "scheduled task registered -> $taskName (starts at logon)"
        return $true
    } catch {
        Write-Warn "Task Scheduler registration failed: $($_.Exception.Message)"
        return $false
    }
}

function Start-Now {
    Stop-RunningGuard
    try {
        Start-Process -FilePath $psExe -ArgumentList @('-NoProfile','-ExecutionPolicy','Bypass','-WindowStyle','Hidden','-File', "`"$guardScript`"") -WindowStyle Hidden
        Write-Step 'guard process launched for this session'
    } catch {
        Write-Warn "could not start it directly: $($_.Exception.Message)"
        try { Start-ScheduledTask -TaskName $taskName; Write-Ok 'started via Task Scheduler' } catch { Write-Warn $_.Exception.Message }
    }
    Start-Sleep -Milliseconds 1500
    $st = Get-HostState
    if ($st.Running.Count -gt 0) {
        Write-Ok "guard is live (PID $(($st.Running | ForEach-Object { $_.ProcessId }) -join ', '))"
    } else {
        Write-Warn 'guard does not appear to be running - check the log:'
        if (Test-Path (Join-Path $logDir 'guard.log')) { Get-Content (Join-Path $logDir 'guard.log') -Tail 12 | ForEach-Object { Write-Host "    $_" } }
    }
}

# ------------------------------------------------------------------------- main
if ($Status)    { Show-Status;   return }
if ($Uninstall) { Remove-Install; return }

if (-not (Test-Path $guardScript)) { throw "wx_alert_guard.ps1 not found next to this script (expected: $guardScript)" }

Write-Host 'Installing the KiCad "wxWidgets Debug Alert" auto-dismiss guard'
Write-Host "  user  : $env:USERDOMAIN\$env:USERNAME"
Write-Host "  host  : $psExe"
Write-Host "  guard : $guardScript"
Write-Host ''

$installed = $false
if (-not $StartupFolderOnly) { $installed = Install-ScheduledTask }
if (-not $installed) {
    Write-Step 'falling back to the per-user Startup folder'
    Install-StartupFolder | Out-Null
}
Start-Now

Write-Host ''
Write-Host 'Behaviour from now on:' -ForegroundColor Green
Write-Host '  * the alert is cancelled automatically within ~0.4s of appearing'
Write-Host '  * wxWidgets then suppresses the remaining warnings for that KiCad session'
Write-Host '  * the guard restarts by itself at every logon'
Write-Host "  * activity log: $(Join-Path $logDir 'guard.log')"
Write-Host ''
Write-Host ('Verify it :  & "' + $guardScript + '" -SelfTest')
Write-Host ('Undo it   :  & "' + $PSCommandPath + '" -Uninstall')
