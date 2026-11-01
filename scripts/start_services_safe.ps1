# Glossa Lab service starter (safe variant) - DELEGATING SHIM.
#
# This file existed because the shipped start_services.ps1 had a
# parser error; both files now delegate to the one canonical
# start, so the distinction no longer exists.
#
# The canonical start is setup-os.cmd (Spec 080): production entry
# (create_app --factory), installed mode (GLOSSA_MODE=installed,
# database under %LOCALAPPDATA%\GlossaLab), and the idempotent,
# identity-checked start. This file used to launch the backend
# directly with the retired non-factory app object and no installed
# mode - the wrong app against the wrong data directory. It now
# delegates; do not add launch logic here. (The -BackendOnly switch
# is retired with the direct launch.)
$setupOs = Join-Path (Split-Path $PSScriptRoot -Parent) "setup-os.cmd"
& cmd.exe /c "`"$setupOs`" start"
exit $LASTEXITCODE
