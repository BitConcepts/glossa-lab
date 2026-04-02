@echo off
REM Glossa Lab - Backend Service Wrapper
REM Single-line uvicorn invocation (no caret continuation).

set "SCRIPT_DIR=%~dp0"
set "REPO_ROOT=%SCRIPT_DIR%.."
for %%I in ("%REPO_ROOT%") do set "REPO_ROOT=%%~fI"

set "VENV_PYTHON=%REPO_ROOT%\backend\venv\Scripts\python.exe"
set "LOG_DIR=%REPO_ROOT%\logs"
set "LOG_FILE=%LOG_DIR%\backend.log"

if not exist "%VENV_PYTHON%" ( echo [ERROR] venv not found. Run setup-os.cmd install first. & exit /b 1 )
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

echo [%DATE% %TIME%] Glossa Lab backend starting... >> "%LOG_FILE%"
"%VENV_PYTHON%" -m uvicorn glossa_lab.main:app --host 127.0.0.1 --port 8001 --app-dir "%REPO_ROOT%\backend" >> "%LOG_FILE%" 2>&1
echo [%DATE% %TIME%] Glossa Lab backend stopped (exit %ERRORLEVEL%). >> "%LOG_FILE%"
exit /b %ERRORLEVEL%
