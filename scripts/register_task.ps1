# register_task.ps1
# Spec 080 FR-004 (Amendment 2, 2026-10-29): register the GlossaLab
# logon task in the route-B shape proven on the desktop host by
# diagnostic glossa-host-diag2-2026-10-28 (run 40816104983):
# a principal scoped to the installing user (Interactive logon
# type, Limited run level) and a logon trigger scoped to that
# user, registered directly in the installer's own non-elevated
# context - NO elevation wrapper. The pre-Amendment-1 shape
# (unscoped AtLogon trigger, no explicit principal, invoked via
# Start-Process -Verb RunAs) is what drew the access denials in
# diagnostic run 40807602846; those denials were shape-caused,
# not a venue-wide bar on per-user task registration.
# H25: Action MUST use wscript.exe + launch-tray.vbs. Never
# cmd.exe or shell.cmd tray.
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$vbs  = Join-Path $PSScriptRoot 'launch-tray.vbs'
$user = $env:USERDOMAIN + '\' + $env:USERNAME
$action    = New-ScheduledTaskAction -Execute 'wscript.exe' -Argument "//nologo `"$vbs`"" -WorkingDirectory $root
$trigger   = New-ScheduledTaskTrigger -AtLogon -User $user
$settings  = New-ScheduledTaskSettingsSet -ExecutionTimeLimit 0 -MultipleInstances IgnoreNew -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
$principal = New-ScheduledTaskPrincipal -UserId $user -LogonType Interactive -RunLevel Limited
Register-ScheduledTask -TaskName 'GlossaLab' -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Force | Out-Null
# Read the registration back: the install is not done until the
# task exists in the Ready state carrying the route-B principal
# and a logon trigger. Any failure above or here throws and the
# installer refuses the install (loud failure, never a skip).
$task = Get-ScheduledTask -TaskName 'GlossaLab'
Write-Host ("GLOSSA_TASK_STATE name=GlossaLab state={0} principal={1} / {2} / {3} trigger={4}" -f $task.State, $task.Principal.UserId, $task.Principal.LogonType, $task.Principal.RunLevel, $task.Triggers[0].CimClass.CimClassName)
if ($task.State -ne 'Ready') {
    Write-Host "[ERROR] GlossaLab task registered but state is '$($task.State)', not 'Ready'."
    exit 1
}
Write-Host 'Task registered. To start the tray now run: wscript.exe //nologo scripts\launch-tray.vbs'
