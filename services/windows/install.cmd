@echo off
REM Glossa Lab — Windows Startup Registration
REM Creates a shortcut in the user's Startup folder to launch the tray app.

set "REPO_ROOT=%~dp0..\.."
set "STARTUP=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "SHORTCUT=%STARTUP%\GlossaLab.lnk"

REM Use PowerShell to create a .lnk shortcut (no .ps1 script — inline only)
powershell -NoProfile -Command ^
  "$ws = New-Object -ComObject WScript.Shell; ^
   $sc = $ws.CreateShortcut('%SHORTCUT%'); ^
   $sc.TargetPath = '%REPO_ROOT%\shell.cmd'; ^
   $sc.Arguments = 'tray'; ^
   $sc.WorkingDirectory = '%REPO_ROOT%'; ^
   $sc.Description = 'Glossa Lab Tray'; ^
   $sc.Save()"

if exist "%SHORTCUT%" (
    echo [OK] Startup shortcut created: %SHORTCUT%
) else (
    echo [ERROR] Failed to create startup shortcut.
    exit /b 1
)
