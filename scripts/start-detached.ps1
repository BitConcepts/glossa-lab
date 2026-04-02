# start-detached.ps1
# Starts a .cmd script fully detached (hidden console, new process group).
# Writes the spawned PID to a file and exits immediately — never hangs.
#
# Usage:
#   powershell -NoProfile -File scripts\start-detached.ps1 `
#       -Script   "C:\path\to\script.cmd" `
#       -PidFile  "C:\path\to\logs\process.pid"
#
# On success: writes PID integer to PidFile, exits 0.
# On failure: writes nothing, exits 1.

param(
    [Parameter(Mandatory)][string]$Script,
    [Parameter(Mandatory)][string]$PidFile
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

try {
    $proc = Start-Process `
        -FilePath    "cmd.exe" `
        -ArgumentList @("/c", "`"$Script`"") `
        -WindowStyle Hidden `
        -PassThru

    $proc.Id | Set-Content -Encoding ASCII -Path $PidFile
    Write-Host $proc.Id
    exit 0
}
catch {
    Write-Error "start-detached.ps1 failed: $_"
    exit 1
}
