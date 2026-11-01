@echo off
REM Glossa Lab - Windows install (Spec 080 FR-004)
REM
REM The ONE canonical Windows installer is setup-os.cmd at the repo
REM root (it registers the GlossaLab scheduled task whose action is
REM wscript.exe + scripts\launch-tray.vbs, per H25). This file only
REM delegates to it. The previous Startup-folder shortcut that
REM pointed at shell.cmd tray violated H25 and is retired; any
REM legacy shortcut is removed by uninstall.cmd / setup-os.cmd.

set "REPO_ROOT=%~dp0..\.."
for %%I in ("%REPO_ROOT%") do set "REPO_ROOT=%%~fI"
call "%REPO_ROOT%\setup-os.cmd" install
exit /b %ERRORLEVEL%
