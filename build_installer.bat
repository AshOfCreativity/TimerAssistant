@echo off
echo Building Timer Assistant...

REM Clean build folders
rmdir /s /q build dist 2>nul
del /f /q TimerAssistant.exe 2>nul

REM Build executable
pyinstaller --clean ^
  --noconsole ^
  --onefile ^
  --name TimerAssistant ^
  --version-file file_version_info.txt ^
  timer_app.py

REM Move executable to current directory
move /y dist\TimerAssistant.exe .\ 2>nul

echo Build completed!
pause