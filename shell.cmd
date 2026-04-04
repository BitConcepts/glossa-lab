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
echo [OK] Backend running on http://localhost:8001 (Ctrl+C to stop)
"%VENV_PYTHON%" -m uvicorn glossa_lab.main:app --host ********* --port 8001 --reload --app-dir "%REPO_ROOT%\backend" %1 %2 %3 %4 %5 %6 %7 %8 %9
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
"%VENV_PYTHON%" -m pip install --upgrade pip
"%VENV_PYTHON%" -m pip install -e "%REPO_ROOT%\backend[dev]"
if exist "%REPO_ROOT%\tray\requirements.txt" (
    "%VENV_PYTHON%" -m pip install -r "%REPO_ROOT%\tray\requirements.txt"
)
if exist "%REPO_ROOT%\frontend\package.json" (
    pushd "%REPO_ROOT%\frontend"
    call npm install
    call npm run build
    popd
)
echo [OK] Dependencies updated.
exit /b 0

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
