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

' Window style 0 = hidden. True = WAIT for the tray to exit and
' propagate its exit code (Spec 080 Amendment 3, 2026-10-29):
' the scheduled task stays Running for the tray's lifetime, so
' the scheduler's restart-on-failure settings supervise the
' tray - a tray crash (nonzero exit) is restarted by the
' scheduler; a clean tray quit (exit 0) is not. A fire-and-
' forget launch made every job-launched start die with its
' launcher and left the scheduler nothing to supervise
' (host runs 40855200786 + 40861773854).
Dim exitCode
exitCode = sh.Run(Chr(34) & pythonw & Chr(34) & " -m glossa_tray", 0, True)
WScript.Quit(exitCode)
