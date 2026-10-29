# Glossa Lab service starter - DELEGATING SHIM.
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
