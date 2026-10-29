' launch-tray.vbs
' Starts the Glossa Lab tray icon with NO visible shell window.
' Usage (agent): wscript.exe //nologo scripts\\launch-tray.vbs
' The tray is launched through wscript.exe, never cmd.exe.
'
' Single-instance: if a glossa_tray process is already running,
' exit 0 without launching a second one (tray processes
' accumulated across repeated starts before this guard - host
' run 40880047294).
'
' Fire-and-forget (Spec 080 Amendment 4, 2026-10-29): this
' launcher does NOT wait on the tray. Amendment 3 made it wait
' so the scheduled task would stay Running and supervise the
' tray; the host diagnosis (task-diag 2026-10-29) proved the
' coupling fatal - the app's own targeted stop kills the tray
' regardless of owner, which ended the task instance with
' LastTaskResult 0xFFFFFFFF, and the task's lifetime bought no
' supervision the tray does not already provide for the
' backend. The task is now a short-lived starter
' (start-ensure.vbs); the tray's lifetime belongs to the tray.

Dim fso, sh, wmi, procs, root, pythonw

Set fso = CreateObject("Scripting.FileSystemObject")
Set sh  = CreateObject("WScript.Shell")

' Derive repo root from this script's location (scripts\ is one level down)
root    = fso.GetParentFolderName(fso.GetParentFolderName(WScript.ScriptFullName))
pythonw = root & "\backend\venv\Scripts\pythonw.exe"

' Single-instance guard: another tray already running -> done.
Set wmi   = GetObject("winmgmts:\\.\root\cimv2")
Set procs = wmi.ExecQuery("SELECT ProcessId FROM Win32_Process WHERE (Name = 'pythonw.exe' OR Name = 'python.exe') AND CommandLine LIKE '%glossa_tray%'")
If procs.Count > 0 Then
    WScript.Quit(0)
End If

' Prepend tray\ to PYTHONPATH so glossa_tray is importable
sh.Environment("PROCESS")("PYTHONPATH") = root & "\tray;" & sh.Environment("PROCESS")("PYTHONPATH")

' Spec 080 FR-005: installed mode for the whole tray process tree, so
' the backend the tray spawns keeps its data under
' %LOCALAPPDATA%\GlossaLab\data regardless of the caller's cwd.
sh.Environment("PROCESS")("GLOSSA_MODE") = "installed"

' Window style 0 = hidden. False = do NOT wait: the tray is a
' detached, scheduler-independent process from here on.
sh.Run Chr(34) & pythonw & Chr(34) & " -m glossa_tray", 0, False
WScript.Quit(0)
