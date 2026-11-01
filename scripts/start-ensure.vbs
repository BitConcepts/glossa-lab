' start-ensure.vbs
' Spec 080 Amendment 4 (2026-10-29): the GlossaLab task's ONE
' action. Runs the installer's idempotent ensure-start
' (setup-os.cmd start) with NO visible window, waits for it,
' and exits with its code. Short-lived BY DESIGN: the task is
' a starter, not a supervisor - it returns to Ready with
' result 0x0 in seconds while the tray and backend it ensured
' live on as detached processes, owned by no task instance
' and no job. Amendment 3's waiting action coupled the task
' instance's lifetime to the tray's, and the app's own
' targeted stop ended the instance with 0xFFFFFFFF when it
' stopped the tray (host task diagnosis, run
' 40855200786 + task-diag 2026-10-29: scheduler events
' 12:24:15 logon fire, LastTaskResult 0xFFFFFFFF).
' setup-os.cmd start is ensure-running: backend healthy with
' verified identity + tray running = no-op exit 0; anything
' missing is launched. Fired at logon, every 15 minutes by
' the task's repetition trigger, and on demand
' (Start-ScheduledTask), it keeps the host's steady state
' without any long-lived instance to assassinate.

Dim fso, sh, root, rc

Set fso = CreateObject("Scripting.FileSystemObject")
Set sh  = CreateObject("WScript.Shell")

' Derive repo root from this script's location (scripts\ is one level down)
root = fso.GetParentFolderName(fso.GetParentFolderName(WScript.ScriptFullName))

' Window style 0 = hidden. True = wait (bounded by the task's
' ExecutionTimeLimit): the starter must report the ensure
' result honestly - exit 0 only when the stack is ensured.
rc = sh.Run("cmd /c " & Chr(34) & root & "\setup-os.cmd" & Chr(34) & " start", 0, True)
WScript.Quit(rc)
