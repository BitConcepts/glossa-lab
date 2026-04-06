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

REM Create (or replace) the single scheduled task.
REM Runs at user logon with a 10-second delay to let the desktop settle.
REM No admin required — runs as current user (LIMITED token).
schtasks /create ^
  /tn "%TASK_NAME%" ^
  /tr "\"%VENV_PYTHONW%\" \"%ENTRY_POINT%\"" ^
  /sc ONLOGON ^
  /delay 0000:10 ^
  /rl LIMITED ^
  /f >nul
if errorlevel 1 (
    echo [ERROR] Failed to create scheduled task. Try running as administrator once.
    exit /b 1
)

echo [OK] Task '%TASK_NAME%' registered — runs at next login.
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
REM Remove legacy HKCU Run entries if present
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "GlossaLabBackend" /f >nul 2>&1
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "GlossaLabTray" /f >nul 2>&1
echo [OK] Uninstalled.
exit /b 0

REM ─────────────────────────────────────────────────────────────
:do_start
REM ─────────────────────────────────────────────────────────────
REM schtasks /run starts a task silently through Task Scheduler service.
REM No console window because: (a) Task Scheduler creates the process
REM outside any console session, (b) pythonw.exe is GUI subsystem.
schtasks /run /tn "%TASK_NAME%" >nul 2>&1
if errorlevel 1 (
    echo [WARN] Task not registered. Run 'setup-os.cmd install' first.
    exit /b 1
)
echo [OK] GlossaLab task started. Tray will appear shortly.
exit /b 0

REM ─────────────────────────────────────────────────────────────
:do_stop
REM ─────────────────────────────────────────────────────────────
call :do_stop_silent
echo [OK] Stopped.
exit /b 0

:do_stop_silent
REM 1. Graceful backend shutdown via HTTP (curl — never hangs PTY)
curl.exe -sf --max-time 3 -X POST "http://localhost:8001/api/v1/shutdown" >nul 2>&1
REM 2. End the scheduled task (kills the tray pythonw.exe process)
schtasks /end /tn "%TASK_NAME%" >nul 2>&1
REM 3. Force-kill any leftover pythonw.exe on the backend port just in case
for /f "tokens=5" %%p in ('netstat -ano 2^>nul ^| findstr ":8001.*LISTENING"') do (
    taskkill /F /PID %%p >nul 2>&1
)
goto :eof

REM ─────────────────────────────────────────────────────────────
:do_restart
REM ─────────────────────────────────────────────────────────────
echo [RESTART] Stopping...
call :do_stop_silent
timeout /t 2 /nobreak >nul
echo [RESTART] Starting...
goto do_start

REM ─────────────────────────────────────────────────────────────
:do_status
REM ─────────────────────────────────────────────────────────────
echo.
echo ── GlossaLab Status ──────────────────────────────────────
schtasks /query /tn "%TASK_NAME%" /fo LIST 2>nul | findstr /i "TaskName Status Last Run"
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
