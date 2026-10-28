@echo off
REM ============================================================
REM Glossa Lab - Desktop Host Installer (Spec 080)
REM ============================================================
REM Idempotent end-to-end install on the desktop host:
REM   1. dependencies (shell.cmd setup) if the venv is missing
REM   2. setup-os.cmd install - the ONE canonical registration
REM      (GlossaLab scheduled task; verifies the tray icon hashes
REM      and fails loudly if they are wrong - FR-005)
REM   3. setup-os.cmd start   - tray via the H25 VBS wrapper,
REM      which starts the backend (production factory entry,
REM      127.0.0.1:8001, GLOSSA_MODE=installed)
REM   4. verify-desktop-host.cmd - identity + supervision proof
REM      (FR-007 markers)
REM ============================================================

setlocal

set "REPO_ROOT=%~dp0.."
for %%I in ("%REPO_ROOT%") do set "REPO_ROOT=%%~fI"

if not exist "%REPO_ROOT%\backend\venv\Scripts\pythonw.exe" (
    echo [SETUP] venv not found - running shell.cmd setup ...
    call "%REPO_ROOT%\shell.cmd" setup
    if errorlevel 1 (
        echo [ERROR] Dependency setup failed.
        exit /b 1
    )
)

call "%REPO_ROOT%\setup-os.cmd" install
if errorlevel 1 (
    echo [ERROR] setup-os.cmd install failed.
    exit /b 1
)

call "%REPO_ROOT%\setup-os.cmd" start
if errorlevel 1 (
    echo [ERROR] setup-os.cmd start failed.
    exit /b 1
)

call "%REPO_ROOT%\scripts\verify-desktop-host.cmd"
set "VERIFY_EXIT=%ERRORLEVEL%"
if not "%VERIFY_EXIT%"=="0" (
    echo [ERROR] Desktop host verification failed ^(exit %VERIFY_EXIT%^).
    exit /b %VERIFY_EXIT%
)

echo [OK] Glossa Lab desktop host installed and verified.
exit /b 0
