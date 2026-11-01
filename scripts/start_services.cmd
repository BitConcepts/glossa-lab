@echo off
REM Glossa Lab service starter - DELEGATING SHIM.
REM
REM The canonical start is setup-os.cmd (Spec 080): production entry
REM (create_app --factory), installed mode (GLOSSA_MODE=installed,
REM database under %LOCALAPPDATA%\GlossaLab), and the idempotent,
REM identity-checked start. This file used to launch the backend
REM directly with the retired non-factory app object and no
REM installed mode - the wrong app against the wrong data
REM directory - and printed [DONE] even when its health check had
REM failed. It now delegates; do not add launch logic here.
call "%~dp0..\setup-os.cmd" start
exit /b %ERRORLEVEL%
