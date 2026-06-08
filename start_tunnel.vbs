Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "cmd.exe /c start /MIN cmd /c ""ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=30 -R 80:localhost:8000 nokey@localhost.run > C:\Users\PC\AppData\Local\Temp\tunnel.log 2>&1""", 0, False
