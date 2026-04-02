@echo off
REM ============================================================
REM Glossa Lab — OS Integration Setup Tool (Windows)
REM ============================================================
REM
REM Usage:
REM   setup-os.cmd install    Install deps + register boot tasks
REM   setup-os.cmd uninstall  Remove boot tasks
REM   setup-os.cmd start      Start the backend (and tray)
REM   setup-os.cmd stop       Stop the backend
REM   setup-os.cmd restart    Restart the backend
REM   setup-os.cmd status     Show current integration status
REM
REM Boot persistence is implemented via Windows Task Scheduler:
REM   - GlossaLabBackend : runs at user logon, starts uvicorn
REM   - GlossaLabTray    : runs at user logon (5s delay), starts tray
REM
REM All Python invocations go through the venv python.exe (never
REM venv\Scripts\*.exe directly — avoids PTY hangs on Windows).
REM ============================================================

setlocal enabledelayedexpansion

set "REPO_ROOT=%~dp0"
REM Remove trailing backslash
if "%REPO_ROOT:~-1%"=="\" set "REPO_ROOT=%REPO_ROOT:~0,-1%"

set "VENV_PYTHON=%REPO_ROOT%\backend\venv\Scripts\python.exe"
set "BACKEND_SVC=%REPO_ROOT%\scripts\run-backend-svc.cmd"
set "TRAY_SVC=%REPO_ROOT%\scripts\run-tray-svc.cmd"
set "LOG_DIR=%REPO_ROOT%\logs"
set "HEALTH_URL=http://localhost:8000/api/v1/health"

set "BACKEND_TASK=GlossaLabBackend"
set "TRAY_TASK=GlossaLabTray"

if "%~1"=="" goto usage
if /i "%~1"=="install"   goto do_install
if /i "%~1"=="uninstall" goto do_uninstall
if /i "%~1"=="start"     goto do_start
if /i "%~1"=="stop"      goto do_stop
if /i "%~1"=="restart"   goto do_restart
if /i "%~1"=="status"    goto do_status
echo [ERROR] Unknown command: %~1
goto usage

REM ─────────────────────────────────────────────────────────────
:do_install
REM ─────────────────────────────────────────────────────────────
echo.
echo [INSTALL] Installing Glossa Lab OS integration...
echo.

REM 1. Install / update all dependencies
echo [1/4] Installing dependencies...
call "%REPO_ROOT%\shell.cmd" setup
if errorlevel 1 ( echo [ERROR] Dependency install failed. & exit /b 1 )
echo [OK] Dependencies installed.

REM 2. Ensure logs directory exists
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"
echo [2/4] Log directory: %LOG_DIR%

REM 3. Register backend in HKCU Run (starts at user login, no admin required)
echo [3/4] Registering backend autostart (HKCU Run)...
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "%BACKEND_TASK%" /t REG_SZ /d "\"%BACKEND_SVC%\"" /f >nul
if errorlevel 1 ( echo [ERROR] Failed to register backend autostart. & exit /b 1 )
echo [OK] Backend registered: HKCU\...\Run\%BACKEND_TASK%

REM 4. Register tray in HKCU Run
echo [4/4] Registering tray autostart (HKCU Run)...
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "%TRAY_TASK%" /t REG_SZ /d "\"%TRAY_SVC%\"" /f >nul
if errorlevel 1 ( echo [ERROR] Failed to register tray autostart. & exit /b 1 )
echo [OK] Tray registered: HKCU\...\Run\%TRAY_TASK%

echo.
echo [INSTALL COMPLETE]
echo   Backend and tray will start automatically at next user login.
echo   To start them right now: setup-os.cmd start
echo.
exit /b 0

REM ─────────────────────────────────────────────────────────────
:do_uninstall
REM ─────────────────────────────────────────────────────────────
echo [UNINSTALL] Removing Glossa Lab OS integration...

call :stop_backend_silent

reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "%BACKEND_TASK%" >nul 2>&1
if not errorlevel 1 (
    reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "%BACKEND_TASK%" /f >nul
    echo [OK] Removed autostart: %BACKEND_TASK%
) else (
    echo [OK] Not registered (nothing to remove): %BACKEND_TASK%
)

reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "%TRAY_TASK%" >nul 2>&1
if not errorlevel 1 (
    reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "%TRAY_TASK%" /f >nul
    echo [OK] Removed autostart: %TRAY_TASK%
) else (
    echo [OK] Not registered (nothing to remove): %TRAY_TASK%
)

REM Also remove the old Startup shortcut if it exists
set "OLD_SHORTCUT=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\GlossaLab.lnk"
if exist "%OLD_SHORTCUT%" (
    del "%OLD_SHORTCUT%"
    echo [OK] Removed legacy startup shortcut.
)

echo [UNINSTALL COMPLETE]
exit /b 0

REM ─────────────────────────────────────────────────────────────
:do_start
REM ─────────────────────────────────────────────────────────────
REM DESIGN: fire-and-forget. Processes are launched fully detached
REM (no console inheritance, new window, hidden). PIDs written to
REM logs\backend.pid and logs\tray.pid. Returns immediately.
REM Use 'setup-os.cmd status' to poll health afterwards.
REM Use 'setup-os.cmd stop' or 'taskkill /F /PID ^<pid^>' to kill.
REM
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

REM ── Backend ──────────────────────────────────────────────────
call :check_health
if "%HEALTH_OK%"=="1" (
    echo [OK] Backend already running at %HEALTH_URL%
    goto do_start_tray
)

echo [START] Launching backend (detached)...
powershell -NoProfile -ExecutionPolicy Bypass -File "%REPO_ROOT%\scripts\start-detached.ps1" -Script "%BACKEND_SVC%" -PidFile "%LOG_DIR%\backend.pid"
if errorlevel 1 ( echo [ERROR] Failed to launch backend. & exit /b 1 )
set /p BACKEND_PID=<"%LOG_DIR%\backend.pid"
echo [OK] Backend launched.
echo      PID  : %BACKEND_PID%
echo      Log  : %LOG_DIR%\backend.log
echo      Kill : taskkill /F /PID %BACKEND_PID%

:do_start_tray
REM ── Tray ─────────────────────────────────────────────────────
echo [START] Launching tray (detached)...
powershell -NoProfile -ExecutionPolicy Bypass -File "%REPO_ROOT%\scripts\start-detached.ps1" -Script "%TRAY_SVC%" -PidFile "%LOG_DIR%\tray.pid"
if errorlevel 1 ( echo [WARN] Tray may not have started. & goto do_start_done )
set /p TRAY_PID=<"%LOG_DIR%\tray.pid"
echo [OK] Tray launched.
echo      PID  : %TRAY_PID%
echo      Log  : %LOG_DIR%\tray.log
echo      Kill : taskkill /F /PID %TRAY_PID%

:do_start_done
echo.
echo Backend is starting. Use 'setup-os.cmd status' to verify health.
echo (Backend typically takes 3-5 seconds to become available.)
exit /b 0

REM ─────────────────────────────────────────────────────────────
:do_stop
REM ─────────────────────────────────────────────────────────────
echo [STOP] Stopping Glossa Lab services...
call :stop_backend_silent
REM Kill tray if PID file exists
if exist "%LOG_DIR%\tray.pid" (
    set /p TRAY_PID=<"%LOG_DIR%\tray.pid"
    taskkill /F /PID !TRAY_PID! >nul 2>&1
    del "%LOG_DIR%\tray.pid" >nul 2>&1
    echo [OK] Tray stopped (PID !TRAY_PID!).
)
echo [OK] Done. Use 'setup-os.cmd status' to verify.
exit /b 0

REM ─────────────────────────────────────────────────────────────
:do_restart
REM ─────────────────────────────────────────────────────────────
echo [RESTART] Restarting...
call :stop_backend_silent
timeout /t 2 /nobreak >nul
goto do_start

REM ─────────────────────────────────────────────────────────────
:do_status
REM ─────────────────────────────────────────────────────────────
call :do_status_inline
exit /b 0

:do_status_inline
echo.
echo ── Glossa Lab Integration Status ─────────────────────────────
REM Check HKCU Run entries
reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "%BACKEND_TASK%" >nul 2>&1
if not errorlevel 1 (
    echo   Backend autostart: registered ^(HKCU Run^)
) else (
    echo   Backend autostart: NOT registered -- run: setup-os.cmd install
)
reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "%TRAY_TASK%" >nul 2>&1
if not errorlevel 1 (
    echo   Tray autostart   : registered ^(HKCU Run^)
) else (
    echo   Tray autostart   : NOT registered -- run: setup-os.cmd install
)
REM Check live health
call :check_health
if "%HEALTH_OK%"=="1" (
    echo   Backend health: RUNNING at %HEALTH_URL%
) else (
    echo   Backend health: NOT RESPONDING at %HEALTH_URL%
)
echo ──────────────────────────────────────────────────────────────
echo.
goto :eof

REM ─────────────────────────────────────────────────────────────
REM Helper: check_health — sets HEALTH_OK=1 if backend responds
REM Uses curl.exe (built-in, Windows 11+) — never hangs PTY.
REM NEVER use PowerShell for/f pipes here (PTY hang — H8 violation).
REM ─────────────────────────────────────────────────────────────
:check_health
set "HEALTH_OK=0"
curl.exe -sf --max-time 3 "%HEALTH_URL%" >nul 2>&1
if not errorlevel 1 set "HEALTH_OK=1"
goto :eof

REM ─────────────────────────────────────────────────────────────
REM Helper: stop_backend_silent
REM Uses curl.exe for shutdown and taskkill for force-kill.
REM NEVER use PowerShell pipes here (PTY hang — H8 violation).
REM ─────────────────────────────────────────────────────────────
:stop_backend_silent
REM Graceful shutdown via API (curl.exe — never hangs)
curl.exe -sf --max-time 3 -X POST "http://localhost:8000/api/v1/shutdown" >nul 2>&1
REM Kill by PID file if available
if exist "%LOG_DIR%\backend.pid" (
    set /p BPID=<"%LOG_DIR%\backend.pid"
    taskkill /F /PID !BPID! >nul 2>&1
    del "%LOG_DIR%\backend.pid" >nul 2>&1
)
goto :eof

REM ─────────────────────────────────────────────────────────────
:usage
REM ─────────────────────────────────────────────────────────────
echo.
echo Glossa Lab OS Integration Tool (Windows)
echo.
echo Usage: setup-os.cmd ^<command^>
echo.
echo Commands:
echo   install    Install deps + register boot tasks (backend + tray)
echo   uninstall  Remove boot tasks
echo   start      Start backend and tray now
echo   stop       Stop backend
echo   restart    Restart backend
echo   status     Show integration status
echo.
echo Boot persistence uses HKCU Run registry key (no admin required).
echo Logs are written to: %REPO_ROOT%\logs\
echo.
exit /b 0
