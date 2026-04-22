# Non-blocking experiment launcher for Glossa Lab
# Usage: .\scripts\run_experiment_bg.ps1 <experiment_id>
# Launches the experiment as a background process and returns immediately.
# Output is logged to logs\exp_<id>.log
param([Parameter(Mandatory=$true)][string]$ExperimentId)

$root   = Split-Path $PSScriptRoot -Parent
$venvPy = $root + '\backend\venv\Scripts\python.exe'
$logs   = $root + '\logs'
if (-not (Test-Path $logs)) { New-Item -ItemType Directory -Path $logs | Out-Null }

$logFile = $logs + '\exp_' + $ExperimentId + '.log'
$args = @('-m', 'glossa_lab.experiments', $ExperimentId)

$proc = Start-Process -FilePath $venvPy `
    -ArgumentList $args `
    -WorkingDirectory ($root + '\backend') `
    -RedirectStandardOutput $logFile `
    -RedirectStandardError  ($logFile + '.err') `
    -PassThru -WindowStyle Hidden

Write-Host "Started experiment '$ExperimentId' (PID $($proc.Id))"
Write-Host "Log: $logFile"
Write-Host "Check results in Glossa Lab UI -> Reports/Data when complete."
