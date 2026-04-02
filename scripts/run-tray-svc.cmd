@echo off
REM Glossa Lab — Tray Service Wrapper
REM Called by the Windows scheduled task "GlossaLabTray" (runs at user logon).
REM Waits a few seconds for the backend to start, then launches the tray icon.

set "SCRIPT_DIR=%~dp0"
set "REPO_ROOT=%SCRIPT_DIR%.."
for %%I in ("%REPO_ROOT%") do set "REPO_ROOT=%%~fI"

set "VENV_PYTHON=%REPO_ROOT%\backend\venv\Scripts\python.exe"
set "TRAY_PATH=%REPO_ROOT%\tray"
set "LOG_DIR=%REPO_ROOT%\logs"
set "LOG_FILE=%LOG_DIR%\tray.log"

if not exist "%VENV_PYTHON%" (
    echo [ERROR] venv not found. Run setup-os.cmd install first.
    exit /b 1
)

if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

REM Brief delay to let the backend scheduled task start first
timeout /t 5 /nobreak >nul

echo [%DATE% %TIME%] Glossa Lab tray starting... >> "%LOG_FILE%"

set "PYTHONPATH=%TRAY_PATH%;%PYTHONPATH%"
"%VENV_PYTHON%" -m glossa_tray >> "%LOG_FILE%" 2>&1

echo [%DATE% %TIME%] Glossa Lab tray stopped (exit %ERRORLEVEL%). >> "%LOG_FILE%"
exit /b %ERRORLEVEL%
