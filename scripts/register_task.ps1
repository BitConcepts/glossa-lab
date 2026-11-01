# register_task.ps1
# Spec 080 FR-004 (Amendment 2, 2026-10-29): register the GlossaLab
# task in the route-B shape proven on the desktop host by
# diagnostic glossa-host-diag2-2026-10-28 (run 40816104983):
# a principal scoped to the installing user (Interactive logon
# type, Limited run level), registered directly in the
# installer's own non-elevated context - NO elevation wrapper.
# The pre-Amendment-1 shape (unscoped AtLogon trigger, no
# explicit principal, invoked via Start-Process -Verb RunAs) is
# what drew the access denials in diagnostic run 40807602846;
# those denials were shape-caused, not a venue-wide bar.
# Amendment 4 (2026-10-29) - the task is a STARTER, not a
# supervisor. Amendment 3's waiting action (launch-tray.vbs
# blocking on the tray, restart-on-failure supervising it)
# coupled the task instance's lifetime to the tray's: the host
# diagnosis (task-diag run, 2026-10-29) showed the app's own
# targeted stop killing the task-owned tray and ending the
# instance with LastTaskResult 0xFFFFFFFF, and a logon-class
# trigger firing a parallel instance at 12:24:15 under a
# Parallel multiple-instances policy then in force. The model
# now: ONE short-lived action (wscript + start-ensure.vbs ->
# setup-os.cmd start, the idempotent ensure), a logon trigger
# for reboots, and a 15-minute repetition trigger as the
# self-heal tick. The action exits with the ensure result in
# seconds; the tray + backend live detached, owned by no task
# instance. Steady state: task Ready, LastTaskResult 0x0.
# Restart-on-failure (3 x 1 min) now covers only starter-launch
# failures. ExecutionTimeLimit 10 minutes bounds the starter
# by construction. MultipleInstances IgnoreNew: starters never
# stack.
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$vbs  = Join-Path $PSScriptRoot 'start-ensure.vbs'
$user = $env:USERDOMAIN + '\' + $env:USERNAME
$action    = New-ScheduledTaskAction -Execute 'wscript.exe' -Argument "//nologo `"$vbs`"" -WorkingDirectory $root
$logon     = New-ScheduledTaskTrigger -AtLogon -User $user
$ensure    = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(2) -RepetitionInterval (New-TimeSpan -Minutes 15) -RepetitionDuration (New-TimeSpan -Days 3650)
$settings  = New-ScheduledTaskSettingsSet -ExecutionTimeLimit (New-TimeSpan -Minutes 10) -MultipleInstances IgnoreNew -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 1)
$principal = New-ScheduledTaskPrincipal -UserId $user -LogonType Interactive -RunLevel Limited
Register-ScheduledTask -TaskName 'GlossaLab' -Action $action -Trigger @($logon, $ensure) -Settings $settings -Principal $principal -Force | Out-Null
# Read the registration back: the install is not done until the
# task exists in the Ready state (the starter's steady state)
# carrying the route-B principal and both triggers. Any failure
# above or here throws and the installer refuses the install
# (loud failure, never a skip).
$task = Get-ScheduledTask -TaskName 'GlossaLab'
$triggerNames = ($task.Triggers | ForEach-Object { $_.CimClass.CimClassName }) -join ','
Write-Host ("GLOSSA_TASK_STATE name=GlossaLab state={0} principal={1} / {2} / {3} trigger={4}" -f $task.State, $task.Principal.UserId, $task.Principal.LogonType, $task.Principal.RunLevel, $triggerNames)
if ($task.State -ne 'Ready') {
    Write-Host "[ERROR] GlossaLab task registered but state is '$($task.State)', not 'Ready'."
    exit 1
}
Write-Host 'Task registered (starter model: logon + 15-minute ensure tick). To start now: setup-os.cmd start'
