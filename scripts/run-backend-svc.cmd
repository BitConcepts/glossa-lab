@echo off
REM Glossa Lab — Backend Service Wrapper
REM Called by the Windows scheduled task "GlossaLabBackend".
REM Runs uvicorn directly via the venv Python and redirects all output
REM to logs\backend.log under the repo root.
REM
REM NEVER invoke venv executables directly — all invocations go through
REM python.exe -m <module> to avoid PTY hangs on Windows.

set "SCRIPT_DIR=%~dp0"
set "REPO_ROOT=%SCRIPT_DIR%.."
REM Normalise path (remove trailing backslash)
for %%I in ("%REPO_ROOT%") do set "REPO_ROOT=%%~fI"

set "VENV_PYTHON=%REPO_ROOT%\backend\venv\Scripts\python.exe"
set "LOG_DIR=%REPO_ROOT%\logs"
set "LOG_FILE=%LOG_DIR%\backend.log"
set "PID_FILE=%LOG_DIR%\backend.pid"

if not exist "%VENV_PYTHON%" (
    echo [ERROR] venv not found at %VENV_PYTHON%
    echo         Run setup-os.cmd install first.
    exit /b 1
)

if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

echo [%DATE% %TIME%] Glossa Lab backend starting... >> "%LOG_FILE%"
echo [%DATE% %TIME%] Python: %VENV_PYTHON% >> "%LOG_FILE%"
echo [%DATE% %TIME%] Working dir: %REPO_ROOT%\backend >> "%LOG_FILE%"

"%VENV_PYTHON%"
    --host 127.0.0.1 ^
    --port 8000 ^
    --app-dir "%REPO_ROOT%\backend" ^
    >> "%LOG_FILE%" 2>&1

echo [%DATE% %TIME%] Glossa Lab backend stopped (exit %ERRORLEVEL%). >> "%LOG_FILE%"
exit /b %ERRORLEVEL%
