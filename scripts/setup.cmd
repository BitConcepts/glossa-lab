@echo off
REM Glossa Lab Setup (Windows)
REM Creates venv, installs backend+dev deps, installs frontend deps.
REM Idempotent — safe to run multiple times.

set "REPO_ROOT=%~dp0.."
set "VENV_PATH=%REPO_ROOT%\backend\venv"
set "VENV_PYTHON=%VENV_PATH%\Scripts\python.exe"

echo === Glossa Lab Setup ===

REM Check Python
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python not found. Install Python 3.11+ and add to PATH.
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version 2^>^&1') do echo [OK] Found %%i

REM Create venv if missing
if not exist "%VENV_PYTHON%" (
    echo [..] Creating virtual environment at backend\venv ...
    python -m venv "%VENV_PATH%"
    echo [OK] Virtual environment created.
) else (
    echo [OK] Virtual environment already exists.
)

REM Install backend deps
if exist "%REPO_ROOT%\backend\pyproject.toml" (
    echo [..] Installing backend dependencies ...
    "%VENV_PYTHON%" -m pip install --quiet --upgrade pip
    "%VENV_PYTHON%" -m pip install --quiet -e "%REPO_ROOT%\backend[dev]"
    echo [OK] Backend dependencies installed.
) else (
    echo [WARN] No backend\pyproject.toml found. Skipping.
)

REM Install frontend deps
if exist "%REPO_ROOT%\frontend\package.json" (
    where npm >nul 2>&1
    if %ERRORLEVEL% equ 0 (
        echo [..] Installing frontend dependencies ...
        pushd "%REPO_ROOT%\frontend"
        call npm install --silent 2>nul
        popd
        echo [OK] Frontend dependencies installed.
    ) else (
        echo [WARN] npm not found. Skipping frontend deps.
    )
) else (
    echo [WARN] No frontend\package.json found. Skipping.
)

echo.
echo === Setup complete ===
echo Run 'shell.cmd run' to start the backend.
