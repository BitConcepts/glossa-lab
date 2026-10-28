' launch-tray.vbs
' Starts the Glossa Lab tray icon with NO visible shell window.
' Usage (agent): wscript.exe //nologo scripts\launch-tray.vbs
' The scheduled task action must also use wscript.exe, never cmd.exe.

Dim fso, sh, root, pythonw

Set fso  = CreateObject("Scripting.FileSystemObject")
Set sh   = CreateObject("WScript.Shell")

' Derive repo root from this script's location (scripts\ is one level down)
root    = fso.GetParentFolderName(fso.GetParentFolderName(WScript.ScriptFullName))
pythonw = root & "\backend\venv\Scripts\pythonw.exe"

' Prepend tray\ to PYTHONPATH so glossa_tray is importable
sh.Environment("PROCESS")("PYTHONPATH") = root & "\tray;" & sh.Environment("PROCESS")("PYTHONPATH")

' Spec 080 FR-005: installed mode for the whole tray process tree, so
' the backend the tray spawns keeps its data under
' %LOCALAPPDATA%\GlossaLab\data regardless of the caller's cwd.
sh.Environment("PROCESS")("GLOSSA_MODE") = "installed"

' Window style 0 = hidden.  False = fire-and-forget (do not wait).
sh.Run Chr(34) & pythonw & Chr(34) & " -m glossa_tray", 0, False
