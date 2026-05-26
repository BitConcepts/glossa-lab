@echo off
REM ============================================================
REM Glossa Lab — OS Integration (Windows)
REM ============================================================
REM
REM One Task Scheduler task (GlossaLab) runs the tray at logon.
REM The tray is the single entry point: it starts the backend
REM automatically if it is not already running.
REM
REM Usage:
REM   setup-os.cmd install    Create/update the GlossaLab scheduled task
REM   setup-os.cmd uninstall  Remove the task and clean up
REM   setup-os.cmd start      Run the task now (tray + backend)
REM   setup-os.cmd stop       Gracefully shut down backend then kill tray
REM   setup-os.cmd restart    Stop then start
REM   setup-os.cmd status     Show task state and backend health
REM ============================================================

setlocal enabledelayedexpansion

set "REPO_ROOT=%~dp0"
if "%REPO_ROOT:~-1%"=="\" set "REPO_ROOT=%REPO_ROOT:~0,-1%"

set "VENV_PYTHONW=%REPO_ROOT%\backend\venv\Scripts\pythonw.exe"
set "ENTRY_POINT=%REPO_ROOT%\tray\start_tray.pyw"
set "LOG_DIR=%REPO_ROOT%\logs"
set "HEALTH_URL=http://localhost:8001/api/v1/health"
set "TASK_NAME=GlossaLab"

if "%~1"==""          goto usage
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
echo [INSTALL] Registering Glossa Lab scheduled task...
echo.

if not exist "%VENV_PYTHONW%" (
    echo [WARN] pythonw.exe not found. Run 'shell.cmd setup' first.
)
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

REM H25: Register via wscript.exe + launch-tray.vbs — no visible window.
REM Supersedes previous HKCU Run approach (used pythonw.exe directly).
REM Remove stale HKCU Run key if present (was causing duplicate launches).
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "%TASK_NAME%" /f >nul 2>&1
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "GlossaLabTray" /f >nul 2>&1

REM Register the scheduled task (requires elevation for ONLOGON trigger).
powershell -NoProfile -Command "Start-Process -FilePath 'powershell.exe' -ArgumentList '-NoProfile -ExecutionPolicy Bypass -File \"%REPO_ROOT%\scripts\register_task.ps1\"' -Verb RunAs -Wait" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Failed to register scheduled task (elevation required).
    exit /b 1
)

echo [OK] '%TASK_NAME%' scheduled task registered — starts at next login.
echo.
echo To start immediately: setup-os.cmd start
echo.
exit /b 0

REM ─────────────────────────────────────────────────────────────
:do_uninstall
REM ─────────────────────────────────────────────────────────────
echo [UNINSTALL] Removing GlossaLab scheduled task...
call :do_stop_silent
schtasks /delete /tn "%TASK_NAME%" /f >nul 2>&1
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "%TASK_NAME%" /f >nul 2>&1
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "GlossaLabBackend" /f >nul 2>&1
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "GlossaLabTray" /f >nul 2>&1
echo [OK] Uninstalled.
exit /b 0

REM ────────────────────────────────────────────────────────────
:do_start
REM ────────────────────────────────────────────────────────────
REM Always stop existing instances first to prevent tray stacking.
call :do_stop_silent
timeout /t 2 /nobreak >nul
REM H25: Launch via wscript.exe + launch-tray.vbs — zero visible window.
wscript.exe //nologo "%REPO_ROOT%\scripts\launch-tray.vbs"
if errorlevel 1 (
    echo [ERROR] Failed to start GlossaLab.
    exit /b 1
)
echo [OK] GlossaLab started. Tray will appear shortly.
exit /b 0

REM ─────────────────────────────────────────────────────────────
:do_stop
REM ─────────────────────────────────────────────────────────────
call :do_stop_silent
echo [OK] Stopped.
exit /b 0

:do_stop_silent
REM 1. Graceful backend shutdown via HTTP
curl.exe -sf --max-time 3 -X POST "http://localhost:8001/api/v1/shutdown" >nul 2>&1
timeout /t 1 /nobreak >nul
REM 2. Kill ALL pythonw.exe instances (tray + any background python GUI)
taskkill /F /IM pythonw.exe >nul 2>&1
REM 3. Force-kill anything still holding port 8001
for /f "tokens=5" %%p in ('netstat -ano 2^>nul ^| findstr ":8001.*LISTENING"') do (
    taskkill /F /PID %%p >nul 2>&1
)
goto :eof

REM ─────────────────────────────────────────────────────────────
:do_restart
REM ─────────────────────────────────────────────────────────────
echo [RESTART] Stopping...
call :do_stop_silent
timeout /t 3 /nobreak >nul
echo [RESTART] Starting...
goto do_start

REM ─────────────────────────────────────────────────────────────
:do_status
REM ─────────────────────────────────────────────────────────────
echo.
echo ── GlossaLab Status ──────────────────────────────────────
schtasks /query /tn "%TASK_NAME%" >nul 2>&1
if not errorlevel 1 (
    echo   Autostart: scheduled task registered
) else (
    echo   Autostart: NOT registered  (run: setup-os.cmd install)
)
echo.
call :check_health
if "%HEALTH_OK%"=="1" (
    echo   Backend: RUNNING at %HEALTH_URL%
) else (
    echo   Backend: NOT RESPONDING at %HEALTH_URL%
)
echo ──────────────────────────────────────────────────────────
echo.
exit /b 0

REM ─────────────────────────────────────────────────────────────
:check_health
set "HEALTH_OK=0"
curl.exe -sf --max-time 3 "%HEALTH_URL%" >nul 2>&1
if not errorlevel 1 set "HEALTH_OK=1"
goto :eof

REM ─────────────────────────────────────────────────────────────
:usage
REM ─────────────────────────────────────────────────────────────
echo.
echo Glossa Lab OS Integration (Windows)
echo.
echo Usage: setup-os.cmd [install ^| uninstall ^| start ^| stop ^| restart ^| status]
echo.
echo  install    Register GlossaLab scheduled task (run once)
echo  uninstall  Remove task and clean up legacy entries
echo  start      Run task now  (tray + backend, no window)
echo  stop       Graceful backend shutdown + kill tray
echo  restart    Stop then start
echo  status     Task state + backend health
echo.
exit /b 0
