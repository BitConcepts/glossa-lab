@echo off
REM Glossa Lab — Remove Windows Startup Registration

set "SHORTCUT=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\GlossaLab.lnk"

if exist "%SHORTCUT%" (
    del "%SHORTCUT%"
    echo [OK] Startup shortcut removed.
) else (
    echo [OK] No startup shortcut found — nothing to remove.
)
