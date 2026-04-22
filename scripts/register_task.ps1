$root   = Split-Path $PSScriptRoot -Parent
$shell  = Join-Path $root 'shell.cmd'
$action = New-ScheduledTaskAction -Execute 'cmd.exe' -Argument ('/c "' + $shell + '" tray') -WorkingDirectory $root
$trigger = New-ScheduledTaskTrigger -AtLogon
$settings = New-ScheduledTaskSettingsSet -ExecutionTimeLimit 0 -MultipleInstances IgnoreNew -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
Register-ScheduledTask -TaskName 'GlossaLab' -Action $action -Trigger $trigger -Settings $settings -RunLevel Limited -Force | Out-Null
Write-Host 'Task registered. Starting now...'
Start-ScheduledTask -TaskName 'GlossaLab'
Write-Host 'Done.'
