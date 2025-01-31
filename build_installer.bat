@echo off
echo Building Timer Assistant...

REM Clean up previous builds
del /f /q TimerAssistant.exe TimerAssistant-Setup.exe 2>nul

REM Build executable
pyinstaller --clean --windowed --onefile --noconsole --name TimerAssistant --distpath=./ --version-file=file_version_info.txt timer_app.py

REM Check if executable was created
if not exist TimerAssistant.exe (
    echo Error: Failed to create executable
    exit /b 1
)

REM Create installer
makensis installer.nsi

REM Check if installer was created
if not exist TimerAssistant-Setup.exe (
    echo Error: Failed to create installer
    exit /b 1
)

echo Build completed successfully!
