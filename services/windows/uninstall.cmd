@echo off
REM Glossa Lab - Windows uninstall (Spec 080 FR-004)
REM Delegates to the canonical installer (setup-os.cmd uninstall)
REM and removes any legacy Startup-folder shortcut left by the
REM retired pre-Spec-080 install path.

set "REPO_ROOT=%~dp0..\.."
for %%I in ("%REPO_ROOT%") do set "REPO_ROOT=%%~fI"
set "SHORTCUT=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\GlossaLab.lnk"

if exist "%SHORTCUT%" (
    del "%SHORTCUT%"
    echo [OK] Legacy Startup shortcut removed.
)
call "%REPO_ROOT%\setup-os.cmd" uninstall
exit /b %ERRORLEVEL%
