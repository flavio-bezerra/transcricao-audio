@echo off
echo Executando o script PowerShell...
PowerShell -ExecutionPolicy Bypass -File "%~dp0setup.ps1"
echo Script concluído!
pause