# Glossa Lab service starter — backend + tray
param([switch]$BackendOnly)

$root   = Split-Path $PSScriptRoot -Parent
$venvPy = "$root\backend\venv\Scripts\python.exe"
$logs   = "$root\logs"

if (-not (Test-Path $logs)) { New-Item -ItemType Directory -Path $logs | Out-Null }

Write-Host "[INFO] Starting Glossa Lab backend (port 8001)..."
$backendArgs = @(
    "-m", "uvicorn", "glossa_lab.main:app",
    "--host", "127.0.0.1",
    "--port", "8001",
    "--app-dir", "$root\backend"
)
$backend = Start-Process -FilePath $venvPy `
    -ArgumentList $backendArgs `
    -WorkingDirectory "$root\backend" `
    -RedirectStandardOutput "$logs\backend.log" `
    -RedirectStandardError  "$logs\backend_err.log" `
    -PassThru -WindowStyle Hidden

Write-Host "[INFO] Backend PID: $($backend.Id)"
Write-Host "[INFO] Waiting 6s for startup..."
Start-Sleep -Seconds 6

# Health check
try {
    $r    = Invoke-WebRequest http://localhost:8001/api/v1/health -UseBasicParsing -TimeoutSec 5
    $data = $r.Content | ConvertFrom-Json
    Write-Host "[OK]   Backend healthy — status=$($data.status) version=$($data.version)"
} catch {
    Write-Host "[WARN] Backend not yet responding. Last log lines:"
    if (Test-Path "$logs\backend.log") {
        Get-Content "$logs\backend.log" | Select-Object -Last 15
    }
    if (Test-Path "$logs\backend_err.log") {
        Get-Content "$logs\backend_err.log" | Select-Object -Last 10
    }
}

if (-not $BackendOnly) {
    Write-Host 'Starting tray...'
    $trayArgs = @('-m', 'glossa_tray')
    $trayLog    = $logs + '\tray.log'
    $trayErrLog = $logs + '\tray_err.log'
    $trayDir    = $root + '\tray'
    $oldPP = $env:PYTHONPATH
    $env:PYTHONPATH = $trayDir + ';' + $oldPP
    $tray = Start-Process -FilePath $venvPy `
        -ArgumentList $trayArgs `
        -WorkingDirectory $root `
        -RedirectStandardOutput $trayLog `
        -RedirectStandardError  $trayErrLog `
        -PassThru -WindowStyle Hidden
    $env:PYTHONPATH = $oldPP
    Write-Host "Tray PID: $($tray.Id)"
}

Write-Host 'Services started. Backend: http://localhost:8001'
