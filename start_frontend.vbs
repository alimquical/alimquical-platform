Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "cmd.exe /c start ""Alimquical Frontend"" /MIN cmd /c ""cd /d ""C:\Users\PC\Documents\EXTERNOS IA\ALIMQUICAL_AI_EXECUTIVE_PLATFORM\frontend"" && pnpm dev --port 3001""", 0, False
