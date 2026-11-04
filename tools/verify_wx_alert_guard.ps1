#requires -Version 5.1
<#
    Verifies the installed KiCad wxWidgets alert guard end to end.

    Each check raises a stand-in "wxWidgets Debug Alert" from THIS process via a
    worker PowerShell that never dismisses anything, so the only thing that can
    close the window is the installed background watchdog.

    Run:  powershell -NoProfile -ExecutionPolicy Bypass -File verify_wx_alert_guard.ps1
#>
$ErrorActionPreference = 'Stop'
$tools = $PSScriptRoot
$guard = Join-Path $tools 'wx_alert_guard.ps1'
$ps    = Join-Path $env:Windir 'System32\WindowsPowerShell\v1.0\powershell.exe'
if (-not (Test-Path $ps)) { $ps = (Get-Command pwsh.exe).Source }

$results = @()

function Invoke-Guard([string[]]$args_) {
    & $ps -NoProfile -ExecutionPolicy Bypass -File $guard @args_ 2>&1 | ForEach-Object { $_.ToString() }
}

Write-Host 'KiCad wxWidgets alert guard - verification'
Write-Host ''

# 1. a watchdog must be installed and running
$out = Invoke-Guard @('-Status')
$running = ($out -join "`n") -match 'GUARD RUNNING'
$results += [pscustomobject]@{ Check = 'background watchdog is running'; Pass = $running; Detail = (($out | Select-Object -First 1)) }
Write-Host ("  [{0}] background watchdog running   {1}" -f $(if ($running) {'OK'} else {'--'}), (($out | Select-Object -First 1)))

# 2. paused guard must leave the alert alone
Invoke-Guard @('-Pause') | Out-Null
$out = Invoke-Guard @('-FakeAlert', '20000', '-ProbeAfter', '3000')
$survived = ($out -join "`n") -match 'still open'
$results += [pscustomobject]@{ Check = '-Pause really leaves alerts up'; Pass = $survived; Detail = (($out | Select-Object -Last 2 | Select-Object -First 1)) }
Write-Host ("  [{0}] -Pause leaves the alert alone  {1}" -f $(if ($survived) {'OK'} else {'XX'}), (($out | Select-Object -Last 2 | Select-Object -First 1)))
Invoke-Guard @('-Resume') | Out-Null

# 3. running guard must auto-cancel the alert
$logFile = Join-Path $env:LOCALAPPDATA 'KiCadWxAlertGuard\guard.log'
$logStart = if (Test-Path $logFile) { @(Get-Content $logFile).Count } else { 0 }
$out = Invoke-Guard @('-FakeAlert', '20000', '-ProbeAfter', '5000')
$cancelled = ($out -join "`n") -match 'closed within'
$secs = 0.0
if (($out -join "`n") -match 'closed within ([0-9.,]+)s') { $secs = [double]($Matches[1].Replace(',','.')) }
$results += [pscustomobject]@{ Check = 'alert is auto-cancelled'; Pass = $cancelled; Detail = (($out | Select-Object -Last 1)) }
Write-Host ("  [{0}] alert auto-cancelled in {1}s   {2}" -f $(if ($cancelled) {'OK'} else {'XX'}), $secs, (($out | Select-Object -Last 1)))

# 4. the guard must press Cancel, never Yes (Yes would hand control to a debugger)
#    - only lines written by this run count, older runs are irrelevant
Start-Sleep -Milliseconds 800
$newLog = if (Test-Path $logFile) { @(Get-Content $logFile | Select-Object -Skip $logStart) } else { @() }
$noEscalation = (($newLog -join "`n") -match 'dismissed') -and (($newLog -join "`n") -notmatch 'WM_CLOSE')
$results += [pscustomobject]@{ Check = 'dismissed at the first level (BM_CLICK)'; Pass = $noEscalation; Detail = 'no WM_CLOSE fallback used' }
Write-Host ("  [{0}] closed by a real button click, no force-close" -f $(if ($noEscalation) {'OK'} else {'!!'}))
$newLog | ForEach-Object { Write-Host "        $_" }

# 5. logon persistence must be wired up
$task = $null
try { $task = Get-ScheduledTask -TaskName 'KiCadWxAlertGuard' -ErrorAction SilentlyContinue } catch { }
$lnk  = Test-Path (Join-Path $env:APPDATA 'Microsoft\Windows\Start Menu\Programs\Startup\KiCadWxAlertGuard.lnk')
$persist = [bool]$task -or $lnk
$results += [pscustomobject]@{ Check = 'restarts at logon'; Pass = $persist; Detail = $(if ($task) { 'scheduled task' } elseif ($lnk) { 'Startup folder entry' } else { 'nothing' }) }
Write-Host ("  [{0}] restarts at logon via {1}" -f $(if ($persist) {'OK'} else {'XX'}), $results[-1].Detail)

Write-Host ''
$failed = @($results | Where-Object { -not $_.Pass })
if ($failed.Count -eq 0) {
    Write-Host ("ALL {0} CHECKS PASSED" -f $results.Count) -ForegroundColor Green
} else {
    Write-Host ("{0} of {1} checks did not pass:" -f $failed.Count, $results.Count) -ForegroundColor Yellow
    $failed | ForEach-Object { Write-Host ("  - {0}  ({1})" -f $_.Check, $_.Detail) }
}
exit $(if ($failed.Count -eq 0) { 0 } else { 1 })
