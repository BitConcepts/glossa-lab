@echo off
REM Glossa Lab Run (Windows)
REM Starts backend and optionally frontend in dev mode.
REM Usage: run.cmd [--frontend] [--all]

set "REPO_ROOT=%~dp0.."
set "VENV_PYTHON=%REPO_ROOT%\backend\venv\Scripts\python.exe"

if not exist "%VENV_PYTHON%" (
    echo [ERROR] Virtual environment not found. Run 'scripts\setup.cmd' first.
    exit /b 1
)

if "%~1"=="--all" goto run_all
if "%~1"=="--frontend" goto run_frontend

REM Default: backend only
echo [OK] Backend running on http://localhost:8000 (Ctrl+C to stop)
"%VENV_PYTHON%" -m uvicorn glossa_lab.main:app --host 127.0.0.1 --port 8000 --reload --app-dir "%REPO_ROOT%\backend"
exit /b %ERRORLEVEL%

:run_frontend
pushd "%REPO_ROOT%\frontend"
call npx vite
popd
exit /b %ERRORLEVEL%

:run_all
start "" "%VENV_PYTHON%" -m uvicorn glossa_lab.main:app --host 127.0.0.1 --port 8000 --reload --app-dir "%REPO_ROOT%\backend"
echo [OK] Backend started in background on http://localhost:8000
pushd "%REPO_ROOT%\frontend"
call npx vite
popd
exit /b %ERRORLEVEL%
