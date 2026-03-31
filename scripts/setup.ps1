#Requires -Version 5.1
<#
.SYNOPSIS
    Sets up the Glossa Lab development environment on Windows.
.DESCRIPTION
    Creates a Python virtual environment, installs backend dependencies,
    and installs frontend dependencies. Idempotent — safe to run multiple times.
#>

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $PSScriptRoot

Write-Host "=== Glossa Lab Setup ===" -ForegroundColor Cyan

# --- Python backend setup ---
$VenvPath = Join-Path $RepoRoot "backend" "venv"
$PythonCmd = if (Get-Command python3 -ErrorAction SilentlyContinue) { "python3" } else { "python" }

# Verify Python is available
try {
    $PyVersion = & $PythonCmd --version 2>&1
    Write-Host "[OK] Found $PyVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python not found. Install Python 3.11+ and ensure it is on PATH." -ForegroundColor Red
    exit 1
}

# Create virtual environment if it doesn't exist
if (-not (Test-Path $VenvPath)) {
    Write-Host "[..] Creating virtual environment at backend/venv ..." -ForegroundColor Yellow
    & $PythonCmd -m venv $VenvPath
    Write-Host "[OK] Virtual environment created." -ForegroundColor Green
} else {
    Write-Host "[OK] Virtual environment already exists." -ForegroundColor Green
}

# Activate and install dependencies
$ActivateScript = Join-Path $VenvPath "Scripts" "Activate.ps1"
. $ActivateScript

$RequirementsFile = Join-Path $RepoRoot "backend" "pyproject.toml"
if (Test-Path $RequirementsFile) {
    Write-Host "[..] Installing backend dependencies ..." -ForegroundColor Yellow
    pip install -e (Join-Path $RepoRoot "backend") --quiet 2>&1 | Out-Null
    Write-Host "[OK] Backend dependencies installed." -ForegroundColor Green
} else {
    Write-Host "[WARN] No backend/pyproject.toml found. Skipping backend deps." -ForegroundColor Yellow
}

# --- Frontend setup ---
$FrontendDir = Join-Path $RepoRoot "frontend"
$PackageJson = Join-Path $FrontendDir "package.json"

if (Test-Path $PackageJson) {
    if (Get-Command npm -ErrorAction SilentlyContinue) {
        Write-Host "[..] Installing frontend dependencies ..." -ForegroundColor Yellow
        Push-Location $FrontendDir
        npm install --silent 2>&1 | Out-Null
        Pop-Location
        Write-Host "[OK] Frontend dependencies installed." -ForegroundColor Green
    } else {
        Write-Host "[WARN] npm not found. Skipping frontend deps. Install Node.js 18+." -ForegroundColor Yellow
    }
} else {
    Write-Host "[WARN] No frontend/package.json found. Skipping frontend deps." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=== Setup complete ===" -ForegroundColor Cyan
Write-Host "Run './scripts/run.ps1' to start the application." -ForegroundColor White
