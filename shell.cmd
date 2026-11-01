@echo off
REM Glossa Lab Shell Wrapper
REM ALL tool invocations MUST go through this file.
REM NEVER call venv\Scripts\*.exe directly.

set "REPO_ROOT=%~dp0"
set "REPO_ROOT=%REPO_ROOT:~0,-1%"
set "VENV_PYTHON=%REPO_ROOT%\backend\venv\Scripts\python.exe"

REM Detect Python command (must be outside if-block to avoid delayed expansion bug)
set "PY=python"
where python3 >nul 2>&1 && set "PY=python3"
REM py launcher takes precedence when available (standard Windows Python installs)
where py >nul 2>&1 && set "PY=py"

REM Bootstrap if venv missing
if not exist "%VENV_PYTHON%" (
    echo [SETUP] Creating venv ...
    %PY% -m venv "%REPO_ROOT%\backend\venv"
    if errorlevel 1 (
        echo [ERROR] Failed to create venv.
        exit /b 1
    )
    "%VENV_PYTHON%" -m pip install --quiet --upgrade pip
    "%VENV_PYTHON%" -m pip install --quiet -e "%REPO_ROOT%\backend[dev]"
    echo [SETUP] Done.
)

if "%~1"=="" goto usage

if /i "%~1"=="test"   goto do_test
if /i "%~1"=="lint"   goto do_lint
if /i "%~1"=="format" goto do_format
if /i "%~1"=="run"    goto do_run
if /i "%~1"=="python" goto do_python
if /i "%~1"=="setup"  goto do_setup
if /i "%~1"=="tray"   goto do_tray
if /i "%~1"=="svc"    goto do_svc
if /i "%~1"=="e2e"    goto do_e2e
goto do_default

:do_test
shift
"%VENV_PYTHON%" -m pytest %1 %2 %3 %4 %5 %6 %7 %8 %9
exit /b %ERRORLEVEL%

:do_lint
shift
"%VENV_PYTHON%" -m ruff check %1 %2 %3 %4 %5 %6 %7 %8 %9
exit /b %ERRORLEVEL%

:do_format
shift
"%VENV_PYTHON%" -m ruff format %1 %2 %3 %4 %5 %6 %7 %8 %9
exit /b %ERRORLEVEL%

:do_run
shift
REM Spec 080 FR-001: production semantics everywhere - app factory,
REM loopback only, no --reload on the production host.
echo [OK] Backend running on http://127.0.0.1:8001 (Ctrl+C to stop)
"%VENV_PYTHON%" -m uvicorn glossa_lab.main:create_app --factory --host 127.0.0.1 --port 8001 --app-dir "%REPO_ROOT%\backend" %1 %2 %3 %4 %5 %6 %7 %8 %9
exit /b %ERRORLEVEL%

:do_python
shift
"%VENV_PYTHON%" %1 %2 %3 %4 %5 %6 %7 %8 %9
exit /b %ERRORLEVEL%

:do_tray
shift
set "PYTHONPATH=%REPO_ROOT%\tray;%PYTHONPATH%"
"%VENV_PYTHON%" -m glossa_tray %1 %2 %3 %4 %5 %6 %7 %8 %9
exit /b %ERRORLEVEL%

:do_svc
shift
call "%REPO_ROOT%\setup-os.cmd" %1 %2 %3 %4 %5 %6 %7 %8 %9
exit /b %ERRORLEVEL%

:do_e2e
shift
pushd "%REPO_ROOT%\frontend"
call npx playwright test %1 %2 %3 %4 %5 %6 %7 %8 %9
set E2E_EXIT=%ERRORLEVEL%
popd
exit /b %E2E_EXIT%

:do_setup
REM Every step is checked: setup used to print "[OK] Dependencies
REM updated." and exit 0 even when a step had failed, so installers
REM calling this script could not tell a broken venv from a good
REM one (2026-10-29 UI-log audit). The failing step is named.
set "SETUP_STEP=pip self-upgrade"
"%VENV_PYTHON%" -m pip install --upgrade pip
if errorlevel 1 goto :setup_fail
set "SETUP_STEP=backend install"
"%VENV_PYTHON%" -m pip install -e "%REPO_ROOT%\backend[dev,tray]"
if errorlevel 1 goto :setup_fail
if not exist "%REPO_ROOT%\tray\requirements.txt" goto :setup_gpu
set "SETUP_STEP=tray requirements"
"%VENV_PYTHON%" -m pip install -r "%REPO_ROOT%\tray\requirements.txt"
if errorlevel 1 goto :setup_fail
:setup_gpu
REM Auto-detect GPU and install the right accelerator package (CuPy for NVIDIA, etc.)
if not exist "%REPO_ROOT%\backend\scripts\install_gpu.py" goto :setup_frontend
set "SETUP_STEP=GPU accelerator install"
"%VENV_PYTHON%" "%REPO_ROOT%\backend\scripts\install_gpu.py"
if errorlevel 1 goto :setup_fail
:setup_frontend
if not exist "%REPO_ROOT%\frontend\package.json" goto :setup_done
pushd "%REPO_ROOT%\frontend"
set "SETUP_STEP=npm install"
call npm install
if errorlevel 1 ( popd & goto :setup_fail )
set "SETUP_STEP=frontend build"
call npm run build
if errorlevel 1 ( popd & goto :setup_fail )
popd
:setup_done
echo [OK] Dependencies updated.
exit /b 0

:setup_fail
echo [ERROR] setup failed during: %SETUP_STEP%. Dependencies were NOT fully updated.
exit /b 1

:do_default
set "CMD=%~1"
shift
"%VENV_PYTHON%" -m %CMD% %1 %2 %3 %4 %5 %6 %7 %8 %9
exit /b %ERRORLEVEL%

:usage
echo Usage: shell.cmd ^<command^> [args]
echo   test [args]    pytest
echo   lint [args]    ruff check
echo   format [args]  ruff format
echo   run [args]     uvicorn backend
echo   python [args]  python in venv
echo   setup          install/update deps
echo   tray           start tray app
echo   svc [cmd]      OS service integration (delegates to setup-os.cmd)
echo   e2e [args]     run Playwright tests (from frontend/)
exit /b 0
