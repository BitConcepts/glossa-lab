# Glossa Lab — non-blocking backend + tray launcher.
# Replacement for start_services.ps1 which has a parser error in the
# shipped copy. Same behaviour: spawns two detached, hidden processes
# (uvicorn + tray) and prints their PIDs, then exits.

param([switch]$BackendOnly)

$root   = Split-Path $PSScriptRoot -Parent
$venvPy = Join-Path $root "backend\venv\Scripts\python.exe"
$logs   = Join-Path $root "logs"
if (-not (Test-Path $logs)) { New-Item -ItemType Directory -Path $logs | Out-Null }

if (-not (Test-Path $venvPy)) {
    Write-Error "venv python not found at $venvPy"
    exit 1
}

# ── Backend (uvicorn) ───────────────────────────────────────────
$backendArgs = @(
    "-m", "uvicorn", "glossa_lab.main:app",
    "--host", "127.0.0.1",
    "--port", "8001",
    "--app-dir", (Join-Path $root "backend")
)
$backend = Start-Process -FilePath $venvPy `
    -ArgumentList $backendArgs `
    -WorkingDirectory (Join-Path $root "backend") `
    -RedirectStandardOutput (Join-Path $logs "backend.log") `
    -RedirectStandardError  (Join-Path $logs "backend_err.log") `
    -PassThru -WindowStyle Hidden
Write-Host ("backend PID: " + $backend.Id)

# ── Wait for the backend to come up, then health probe ────────────
Start-Sleep -Seconds 6
try {
    $r = Invoke-WebRequest "http://127.0.0.1:8001/api/v1/health" -UseBasicParsing -TimeoutSec 5
    Write-Host ("backend health: " + $r.Content)
} catch {
    Write-Host ("backend not responding yet (will keep starting): " + $_.Exception.Message)
}

# ── Tray ──────────────────────────────────────────────────────────
if (-not $BackendOnly) {
    $env:PYTHONPATH = (Join-Path $root "tray") + ";" + $env:PYTHONPATH
    $tray = Start-Process -FilePath $venvPy `
        -ArgumentList @("-m", "glossa_tray") `
        -WorkingDirectory $root `
        -RedirectStandardOutput (Join-Path $logs "tray.log") `
        -RedirectStandardError  (Join-Path $logs "tray_err.log") `
        -PassThru -WindowStyle Hidden
    Write-Host ("tray PID: " + $tray.Id)
}

Write-Host ("logs: " + $logs)
Write-Host "Detached. This launcher exits now."
