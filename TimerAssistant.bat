@echo off
title Timer Assistant
echo Starting Timer Assistant...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH.
    echo Please install Python from https://python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

REM Check if required packages are available
python -c "import tkinter; import threading; import time; import re" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install word2number
)

REM Run the timer application
echo Launching Timer Assistant...
python timer_app.py

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo There was an error running the Timer Assistant.
    pause
)