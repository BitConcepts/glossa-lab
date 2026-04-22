@echo off
REM Start Glossa Lab backend + tray in the background

set "ROOT=%~dp0.."
set "VENV_PY=%ROOT%\backend\venv\Scripts\python.exe"
set "LOGS=%ROOT%\logs"

if not exist "%LOGS%" mkdir "%LOGS%"

echo [INFO] Starting backend on http://localhost:8001 ...
start "GlossaBackend" /B "%VENV_PY%" -m uvicorn glossa_lab.main:app --host 127.0.0.1 --port 8001 --app-dir "%ROOT%\backend" > "%LOGS%\backend.log" 2> "%LOGS%\backend_err.log"

echo [INFO] Waiting 7 seconds for startup...
timeout /t 7 /nobreak >nul

REM Health check
"%VENV_PY%" -c "import urllib.request; r=urllib.request.urlopen('http://localhost:8001/api/v1/health',timeout=5); print('[OK] Backend health:', r.read().decode()[:120])" 2>nul || echo [WARN] Backend not responding yet - check logs\backend_err.log

echo [INFO] Starting tray...
set "PYTHONPATH=%ROOT%\tray;%PYTHONPATH%"
start "GlossaTray" /B "%VENV_PY%" -m glossa_tray > "%LOGS%\tray.log" 2> "%LOGS%\tray_err.log"

echo [DONE] Services started.
echo   Backend:  http://localhost:8001
echo   Log dir:  %LOGS%
