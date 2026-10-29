@echo off
REM ============================================================
REM Glossa Lab — OS Integration (Windows)
REM ============================================================
REM
REM One Task Scheduler task (GlossaLab) is the host's starter
REM (Spec 080 FR-004, Amendment 4, 2026-10-29): registered by
REM scripts\register_task.ps1 in the route-B shape (scoped
REM principal, Interactive / Limited, no elevation), its one
REM short-lived action runs the idempotent ensure-start
REM (scripts\start-ensure.vbs -> this file's start) at logon
REM and on a 15-minute repetition tick. It supervises nothing
REM itself; the tray + backend live detached (see the spec).
REM The tray is the single entry point: it starts the backend
REM automatically if it is not already running, and on Windows it
REM supervises it (Spec 080: capped auto-restart, never overriding
REM a user stop).
REM
REM This file is the ONE canonical Windows installer (Spec 080
REM FR-004). services\windows\install.cmd delegates here.
REM
REM Usage:
REM   setup-os.cmd install    Create/update the GlossaLab scheduled task
REM   setup-os.cmd uninstall  Remove the task and clean up
REM   setup-os.cmd start      Start the tray now (tray + backend)
REM   setup-os.cmd stop       Gracefully shut down backend then stop tray
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

REM Spec 080 FR-007: the installer verifies the packaged tray icon
REM assets by SHA-256 and fails loudly on any mismatch. These pins
REM are the Spec 079 packaged assets; if the icon is ever re-cut,
REM update the pins here, in scripts\verify_desktop_host.py, and in
REM specs\080-desktop-host-migration in the same change.
set "ICON_ICO=%REPO_ROOT%\tray\glossa_tray\assets\glossa-lab.ico"
set "ICON_ICO_SHA256=315940742D75720388264DCDF03178C58F878EA0701D03EEBA95688D935FF520"
set "ICON_PNG=%REPO_ROOT%\tray\glossa_tray\assets\glossa-lab.png"
set "ICON_PNG_SHA256=BB41BF09D4177CEE0C96B29EBE480F86A9E7115946F9E4AD132D2367A7ADB077"

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
echo [INSTALL] Registering Glossa Lab autostart...
echo.

if not exist "%VENV_PYTHONW%" (
    echo [SETUP] venv not found - running 'shell.cmd setup' ^(backend + tray^)...
    call "%REPO_ROOT%\shell.cmd" setup
    if errorlevel 1 (
        echo [ERROR] shell.cmd setup failed - dependencies were NOT installed. Aborting install.
        exit /b 1
    )
)
if not exist "%VENV_PYTHONW%" (
    echo [ERROR] pythonw.exe still not found after setup. Install Python 3 and retry.
    exit /b 1
)
if not exist "%ICON_ICO%" (
    echo [ERROR] Glossa Lab tray icon asset missing: tray\glossa_tray\assets\glossa-lab.ico
    exit /b 1
)
if not exist "%ICON_PNG%" (
    echo [ERROR] Glossa Lab tray icon asset missing: tray\glossa_tray\assets\glossa-lab.png
    exit /b 1
)
REM Verify both icon assets against the pinned SHA-256 hashes.
REM The comparison lives in scripts\verify_icon_hashes.ps1, which
REM hashes with the .NET SHA-256 implementation. The previous
REM inline Get-FileHash one-liner depended on module autoloading:
REM in the Syncyard runner's powershell.exe -NoProfile context
REM (2026-10-28) Get-FileHash threw CommandNotFoundException, and
REM this check then misreported that hashing failure as a hash
REM mismatch and refused a good install. The helper compares
REM case-insensitively (a hex digest's letter case carries no
REM information) and distinguishes "could not hash" from
REM "mismatch"; any nonzero exit refuses the install, loudly.
powershell -NoProfile -ExecutionPolicy Bypass -File "%REPO_ROOT%\scripts\verify_icon_hashes.ps1" -IcoPath "%ICON_ICO%" -IcoSha256 "%ICON_ICO_SHA256%" -PngPath "%ICON_PNG%" -PngSha256 "%ICON_PNG_SHA256%"
if errorlevel 1 (
    echo [ERROR] Tray icon verification failed - refusing to install.
    exit /b 1
)
echo [OK] Tray icon assets verified ^(SHA-256^).
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

REM H25: the task action launches via wscript.exe + launch-tray.vbs -
REM no visible window. Registration is the route-B shape (Spec 080
REM FR-004, Amendment 2): scripts\register_task.ps1 registers the
REM GlossaLab task with a principal scoped to the installing user
REM (Interactive / Limited) and a logon trigger scoped to that
REM user, in THIS context - no elevation wrapper. The script reads
REM the task back and prints GLOSSA_TASK_STATE; a registration or
REM read-back failure exits nonzero and refuses the install.
REM Remove stale HKCU Run values from retired mechanisms (incl.
REM the Amendment 1 Run-key route): cleanup only, never a route.
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "%TASK_NAME%" /f >nul 2>&1
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "GlossaLabTray" /f >nul 2>&1
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "GlossaLabBackend" /f >nul 2>&1
powershell -NoProfile -ExecutionPolicy Bypass -File "%REPO_ROOT%\scripts\register_task.ps1"
if errorlevel 1 (
    echo [ERROR] Failed to register the GlossaLab scheduled task.
    exit /b 1
)
echo [OK] '%TASK_NAME%' scheduled task registered - starter armed (logon + 15-minute ensure tick).

REM Spec 082 (T011): provision this install's API token before the
REM first start. The token module creates the installed data dir's
REM api_token file atomically (mode owner-only where the platform
REM supports it) when absent and leaves an existing token untouched;
REM its output is the token file's PATH plus a fingerprint - never
REM the value. A failure here refuses the install loudly rather
REM than leaving a backend no client can authenticate to.
set "PYTHONPATH=%REPO_ROOT%\backend"
set "GLOSSA_MODE=installed"
"%REPO_ROOT%\backend\venv\Scripts\python.exe" -m glossa_lab.auth ensure
if errorlevel 1 (
    echo [ERROR] API token provisioning failed - refusing to install.
    exit /b 1
)
set "GLOSSA_MODE="
set "PYTHONPATH="
echo [OK] API token provisioned for this install (path only, above).
echo.
echo To start immediately: setup-os.cmd start
echo.
exit /b 0

REM ─────────────────────────────────────────────────────────────
:do_uninstall
REM ─────────────────────────────────────────────────────────────
echo [UNINSTALL] Removing GlossaLab autostart...
call :do_stop_silent
schtasks /delete /tn "%TASK_NAME%" /f >nul 2>&1
REM HKCU Run deletes below are legacy cleanup (retired mechanisms).
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "%TASK_NAME%" /f >nul 2>&1
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "GlossaLabBackend" /f >nul 2>&1
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "GlossaLabTray" /f >nul 2>&1
echo [OK] Uninstalled.
exit /b 0

REM ────────────────────────────────────────────────────────────
:do_start
REM ────────────────────────────────────────────────────────────
REM Idempotent start (Spec 080 Amendment 3, 2026-10-29): if the
REM backend already answers healthy WITH the Spec 079 identity
REM (bounded healthcheck.py: /docs 200 + health + OpenAPI title),
REM the start is a no-op success. The previous stop-first-always
REM shape let two starts race a second backend into an
REM address-in-use exit (host run 40861773854 log evidence).
if exist "%REPO_ROOT%\backend\venv\Scripts\python.exe" (
    "%REPO_ROOT%\backend\venv\Scripts\python.exe" "%REPO_ROOT%\services\linux\healthcheck.py" --attempts 2 >nul 2>&1
    if not errorlevel 1 (
        REM Backend identity verified. Ensure the TRAY too
        REM (Amendment 3): if a venv-python tray process is
        REM already running, the start is a full no-op; if not,
        REM launch ONLY the tray - never a second backend, never
        REM a stop. (Tray processes accumulated across repeated
        REM starts before this gate: host run 40880047294.)
        powershell -NoProfile -NonInteractive -Command "if (Get-CimInstance Win32_Process | Where-Object { $_.ExecutablePath -match 'venv\\Scripts\\python' -and $_.CommandLine -match 'glossa_tray' }) { exit 0 } else { exit 1 }" >nul 2>&1
        if not errorlevel 1 (
            echo GLOSSA_START_STATE already-running identity=verified tray=running
            echo [OK] GlossaLab backend and tray already running - start is a no-op.
            exit /b 0
        )
        echo GLOSSA_START_STATE tray-launched backend=already-running
        wscript.exe //nologo "%REPO_ROOT%\scripts\launch-tray.vbs"
        echo [OK] Backend already running with verified identity; tray launched.
        exit /b 0
    )
)
REM Always stop existing instances first to prevent tray stacking.
call :do_stop_silent
REM Waits use ping, not timeout.exe: timeout errors out under
REM redirected stdin ("Input redirection is not supported"),
REM printing ERROR lines into successful job logs.
ping -n 3 127.0.0.1 >nul
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
REM Spec 080 FR-003: targeted stop only. The previous version killed
REM EVERY pythonw.exe on the machine; that is gone. Only processes
REM that are verifiably Glossa's are touched, in this order:
REM   1. the tray (H25 stop-tray.vbs targets -m glossa_tray only) —
REM      first, so the tray's auto-restart cannot resurrect the
REM      backend while it is being stopped;
REM   2. the backend, gracefully, via its shutdown endpoint;
REM   3. a bounded wait (H11: ~20 s) for port 8001 to drain;
REM   4. only a process still listening on 8001 whose command line
REM      matches glossa_lab + uvicorn is force-killed, by PID.
wscript.exe //nologo "%REPO_ROOT%\scripts\stop-tray.vbs" >nul 2>&1
REM Spec 082 (T011): the shutdown endpoint is token-gated. When
REM this install's token file exists, present the token as the
REM Bearer header; when it does not, send the bare request exactly
REM as before - the bounded drain + verified kill below remains
REM the last resort either way. The value is read into a variable
REM for this one call and cleared after; it is never echoed.
set "GLOSSA_TOKEN="
if exist "%LOCALAPPDATA%\GlossaLab\data\api_token" set /p GLOSSA_TOKEN=<"%LOCALAPPDATA%\GlossaLab\data\api_token"
if defined GLOSSA_TOKEN (
    curl.exe -sf --max-time 3 -X POST -H "Authorization: Bearer %GLOSSA_TOKEN%" "http://localhost:8001/api/v1/shutdown" >nul 2>&1
) else (
    curl.exe -sf --max-time 3 -X POST "http://localhost:8001/api/v1/shutdown" >nul 2>&1
)
set "GLOSSA_TOKEN="
REM Drain test targets the LOOPBACK listener only: the
REM Tailscale Serve proxy holds its own tailnet :8001
REM listener forever, so an unqualified :8001 test never
REM drains on this host (Defect 1 context, 2026-10-29).
set "STOP_WAITS=0"
:stop_wait_loop
netstat -ano 2>nul | findstr "127.0.0.1:8001.*LISTENING" >nul 2>&1
if errorlevel 1 goto :eof
set /a STOP_WAITS+=1
if !STOP_WAITS! GEQ 10 (
    for /f "tokens=5" %%p in ('netstat -ano 2^>nul ^| findstr "127.0.0.1:8001.*LISTENING"') do (
        powershell -NoProfile -Command "$p = Get-CimInstance Win32_Process -Filter 'ProcessId = %%p' -ErrorAction SilentlyContinue; if ($p -and $p.CommandLine -match 'glossa_lab' -and $p.CommandLine -match 'uvicorn') { Stop-Process -Id %%p -Force -ErrorAction SilentlyContinue }"
    )
    goto :eof
)
ping -n 3 127.0.0.1 >nul
goto stop_wait_loop

REM ─────────────────────────────────────────────────────────────
:do_restart
REM ─────────────────────────────────────────────────────────────
echo [RESTART] Stopping...
call :do_stop_silent
ping -n 4 127.0.0.1 >nul
echo [RESTART] Starting...
goto do_start

REM ─────────────────────────────────────────────────────────────
:do_status
REM ─────────────────────────────────────────────────────────────
echo.
echo ── GlossaLab Status ──────────────────────────────────────
schtasks /query /tn "%TASK_NAME%" >nul 2>&1
if not errorlevel 1 (
    echo   Autostart: GlossaLab scheduled task registered
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
echo  install    Register the GlossaLab scheduled task (run once)
echo  uninstall  Remove the scheduled task and clean up legacy entries
echo  start      Start tray now  (tray + backend, no window)
echo  stop       Graceful backend shutdown + stop tray (targeted)
echo  restart    Stop then start
echo  status     Autostart state + backend health
echo.
exit /b 0
