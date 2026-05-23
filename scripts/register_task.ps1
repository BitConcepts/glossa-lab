# register_task.ps1
# H25: Action MUST use wscript.exe + launch-tray.vbs. Never cmd.exe or shell.cmd tray.
$root   = Split-Path $PSScriptRoot -Parent
$vbs    = Join-Path $PSScriptRoot 'launch-tray.vbs'
$action = New-ScheduledTaskAction -Execute 'wscript.exe' -Argument "//nologo `"$vbs`"" -WorkingDirectory $root
$trigger  = New-ScheduledTaskTrigger -AtLogon
$settings = New-ScheduledTaskSettingsSet -ExecutionTimeLimit 0 -MultipleInstances IgnoreNew -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
Register-ScheduledTask -TaskName 'GlossaLab' -Action $action -Trigger $trigger -Settings $settings -RunLevel Limited -Force | Out-Null
Write-Host 'Task registered. To start the tray now run: wscript.exe //nologo scripts\launch-tray.vbs'
