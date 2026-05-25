' stop-tray.vbs
' Stops the Glossa Lab tray icon with NO visible shell window.
' Usage (agent): wscript.exe //nologo scripts\stop-tray.vbs
' Waits for the kill to complete before returning (True = wait).

Dim sh
Set sh = CreateObject("WScript.Shell")

' Window style 0 = hidden.  True = wait for PowerShell to complete (synchronous).
' Stop-Process -Force is synchronous; covers both the py.exe launcher and the scoop worker.
sh.Run "powershell -NoProfile -NonInteractive -Command ""Get-WmiObject Win32_Process | Where-Object { $_.Name -eq 'pythonw.exe' -and $_.CommandLine -like '*-m glossa_tray*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }""", 0, True
