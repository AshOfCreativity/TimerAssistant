@echo off
echo Building Timer Assistant Installer...

REM Copy the executable to the windows build directory
copy ..\dist\TimerAssistant.exe TimerAssistant.exe

REM Build the installer
makensis installer.nsi

echo Installer creation complete!
echo You can find the installer at: TimerAssistant-Setup.exe
