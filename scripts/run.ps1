#Requires -Version 5.1
<#
.SYNOPSIS
    Starts Glossa Lab in development mode on Windows.
.DESCRIPTION
    Activates the Python virtual environment and starts the backend server.
    Optionally starts the frontend dev server in a separate process.
.PARAMETER Backend
    Start only the backend (default if no flags given).
.PARAMETER Frontend
    Start only the frontend dev server.
.PARAMETER All
    Start both backend and frontend.
#>

param(
    [switch]$Backend,
    [switch]$Frontend,
    [switch]$All
)

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $PSScriptRoot

# Default to backend-only if no flags
if (-not $Backend -and -not $Frontend -and -not $All) {
    $Backend = $true
}
if ($All) {
    $Backend = $true
    $Frontend = $true
}

# --- Backend ---
if ($Backend) {
    $VenvPath = Join-Path $RepoRoot "backend" "venv"
    $ActivateScript = Join-Path $VenvPath "Scripts" "Activate.ps1"

    if (-not (Test-Path $ActivateScript)) {
        Write-Host "[ERROR] Virtual environment not found. Run './scripts/setup.ps1' first." -ForegroundColor Red
        exit 1
    }

    . $ActivateScript

    Write-Host "[..] Starting Glossa Lab backend ..." -ForegroundColor Cyan
    $BackendDir = Join-Path $RepoRoot "backend"

    if ($Frontend) {
        # Start backend in background if we also need frontend
        Start-Process -NoNewWindow -FilePath python -ArgumentList "-m", "uvicorn", "glossa_lab.main:app", "--host", "127.0.0.1", "--port", "8000", "--reload" -WorkingDirectory $BackendDir
        Write-Host "[OK] Backend started in background on http://localhost:8000" -ForegroundColor Green
    } else {
        # Start backend in foreground (blocks)
        Write-Host "[OK] Backend running on http://localhost:8000 (Ctrl+C to stop)" -ForegroundColor Green
        python -m uvicorn glossa_lab.main:app --host 127.0.0.1 --port 8000 --reload
    }
}

# --- Frontend ---
if ($Frontend) {
    $FrontendDir = Join-Path $RepoRoot "frontend"
    $PackageJson = Join-Path $FrontendDir "package.json"

    if (-not (Test-Path $PackageJson)) {
        Write-Host "[ERROR] No frontend/package.json found. Run './scripts/setup.ps1' first." -ForegroundColor Red
        exit 1
    }

    Write-Host "[..] Starting frontend dev server ..." -ForegroundColor Cyan
    Push-Location $FrontendDir
    npm run dev
    Pop-Location
}
