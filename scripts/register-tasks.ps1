# register-tasks.ps1
# Called by setup-os.cmd to register Windows Task Scheduler tasks.
# Usage: powershell -File register-tasks.ps1 -BackendSvc <path> -TraySvc <path>
param(
    [Parameter(Mandatory)][string]$BackendSvc,
    [Parameter(Mandatory)][string]$TraySvc,
    [string]$BackendTask = "GlossaLabBackend",
    [string]$TrayTask    = "GlossaLabTray"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Register-GlossaTask {
    param(
        [string]$TaskName,
        [string]$WrapperPath
    )

    # Remove existing task silently
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue

    $action   = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"$WrapperPath`""
    $trigger  = New-ScheduledTaskTrigger -AtLogOn
    $settings = New-ScheduledTaskSettingsSet `
                    -ExecutionTimeLimit ([TimeSpan]::Zero) `
                    -MultipleInstances  IgnoreNew `
                    -StartWhenAvailable

    Register-ScheduledTask `
        -TaskName $TaskName `
        -Action   $action `
        -Trigger  $trigger `
        -Settings $settings `
        -Force | Out-Null

    Write-Host "[OK] Task registered: $TaskName"
}

Register-GlossaTask -TaskName $BackendTask -WrapperPath $BackendSvc
Register-GlossaTask -TaskName $TrayTask    -WrapperPath $TraySvc
Write-Host "[OK] Both tasks registered successfully."
