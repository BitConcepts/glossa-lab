@echo off
REM Glossa Lab - Desktop Host Verification (Spec 080 FR-007)
REM Thin wrapper: all logic lives in verify_desktop_host.py so the
REM checks are unit-testable. Emits GLOSSA_* marker lines.

set "REPO_ROOT=%~dp0.."
for %%I in ("%REPO_ROOT%") do set "REPO_ROOT=%%~fI"

set "VENV_PYTHON=%REPO_ROOT%\backend\venv\Scripts\python.exe"
if not exist "%VENV_PYTHON%" (
    echo GLOSSA_HOST_VERIFY result=FAIL reason=venv-missing
    echo [ERROR] venv not found. Run scripts\install-desktop-host.cmd first.
    exit /b 1
)

"%VENV_PYTHON%" "%REPO_ROOT%\scripts\verify_desktop_host.py" %1 %2 %3 %4 %5 %6 %7 %8 %9
exit /b %ERRORLEVEL%
