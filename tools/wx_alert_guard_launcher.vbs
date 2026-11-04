' Starts the KiCad wxWidgets Debug Alert guard with no visible window.
Option Explicit
Dim shell, cmd
Set shell = CreateObject("WScript.Shell")
cmd = """C:\WINDOWS\System32\WindowsPowerShell\v1.0\powershell.exe"" -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File ""C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\tools\wx_alert_guard.ps1"""
shell.Run cmd, 0, false
