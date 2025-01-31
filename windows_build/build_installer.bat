@echo off
setlocal enabledelayedexpansion

echo Building Timer Assistant Installer...

REM Ensure output directories exist
if not exist "dist" mkdir dist
if not exist "build" mkdir build

REM Copy the executable and dependencies
echo Copying files...
copy /Y "..\dist\TimerAssistant.exe" "TimerAssistant.exe"

REM Build the installer
echo Building installer...
makensis installer.nsi
if errorlevel 1 (
    echo Error: Installer creation failed!
    exit /b 1
)

REM Move the installer to dist directory
echo Moving installer to dist directory...
move "TimerAssistant-Setup.exe" "..\dist\TimerAssistant-Setup.exe"

echo Installation package created successfully!
echo You can find the installer at: dist\TimerAssistant-Setup.exe

exit /b 0