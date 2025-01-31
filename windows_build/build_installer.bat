@echo off
echo Building Timer Assistant...

REM Clean build folders
rmdir /s /q build dist 2>nul
del /f /q TimerAssistant.exe TimerAssistant-Setup.exe 2>nul

REM Build executable using spec file
echo Building executable...
pyinstaller --clean timer_app.spec

REM Check if build succeeded
if not exist "dist\TimerAssistant.exe" (
    echo Error: Build failed!
    exit /b 1
)

REM Move executable and required files
echo Moving files...
move /y dist\TimerAssistant.exe .\ 2>nul
if not exist "TimerAssistant.exe" (
    echo Error: Failed to move executable!
    exit /b 1
)

REM Build installer
echo Building installer...
if exist "C:\Program Files (x86)\NSIS\makensis.exe" (
    "C:\Program Files (x86)\NSIS\makensis.exe" installer.nsi
) else if exist "C:\Program Files\NSIS\makensis.exe" (
    "C:\Program Files\NSIS\makensis.exe" installer.nsi
) else (
    echo Error: NSIS not found! Please install NSIS to create the installer.
    echo You can download NSIS from https://nsis.sourceforge.io/
    exit /b 1
)

if exist "TimerAssistant-Setup.exe" (
    echo Build completed successfully!
    echo Installer created: TimerAssistant-Setup.exe
) else (
    echo Error: Installer creation failed!
    exit /b 1
)