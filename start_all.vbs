Set WshShell = CreateObject("WScript.Shell")
WshShell.Run chr(34) & "C:\Users\PC\Documents\EXTERNOS IA\ALIMQUICAL_AI_EXECUTIVE_PLATFORM\start_backend.bat" & Chr(34), 0, False
WScript.Sleep 5000
WshShell.Run chr(34) & "C:\Users\PC\Documents\EXTERNOS IA\ALIMQUICAL_AI_EXECUTIVE_PLATFORM\start_frontend.bat" & Chr(34), 0, False
