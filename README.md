# Timer Management Application

A text-based timer management application that allows you to create and manage multiple timers through text commands or a graphical interface.

## Features

- Create named timers with specific durations
- Start, pause, resume, and stop timers
- List all timers and their current status
- Desktop notifications and sound alerts when timers complete
- Natural language command support
- Side panel display of active timers
- Command-line interface for all operations

## Download and Installation

### Windows Users (Recommended)

1. Download `TimerAssistant.exe` from the releases page
2. Double-click to run the application
3. No additional installation required

### Building from Source (Windows)

If you want to build the executable yourself:

1. Install Python 3.6 or higher from [python.org](https://python.org)
   - During installation, check "Add Python to PATH"

2. Install Sox:
   - Download Sox for Windows from [SourceForge](https://sourceforge.net/projects/sox/files/sox/)
   - Install to default location (`C:\Program Files (x86)\sox-14.4.2\`)

3. Open Command Prompt as Administrator and run:
   ```cmd
   pip install pyinstaller word2number
   ```

4. Navigate to the project directory and run:
   ```cmd
   pyinstaller timer.spec
   ```

5. Find the executable in the `dist` folder

### Linux

1. Install Python 3.6 or higher:
   ```bash
   sudo apt-get update
   sudo apt-get install python3 python3-pip python3-tk
   ```

2. Install Sox:
   ```bash
   sudo apt-get install sox
   ```

3. Install required Python packages:
   ```bash
   pip3 install word2number
   ```

### macOS

1. Install Python 3.6 or higher:
   - Download from [python.org](https://python.org), or
   - Use Homebrew: `brew install python3`

2. Install Sox:
   ```bash
   brew install sox
   ```

3. Install required Python packages:
   ```bash
   pip3 install word2number
   ```

## Usage

1. Start the application by running `TimerAssistant.exe` (Windows) or `python timer_app.py` (Linux/macOS).
2. Type `help` to see available commands

### Example Commands

- "set a 5 minute timer for coffee break"
- "start a 25 min pomodoro timer"
- "create 1 hour meeting timer"
- "pause the coffee timer"
- "show all timers"
- "stop meeting timer"

The application will understand your intent and execute the command.

## Offline Use

This application works completely offline. Once downloaded, no internet connection is required.

## Troubleshooting

### No Sound Alerts

The application uses built-in sound alerts. If you don't hear alerts:
1. Check Windows sound settings
2. Ensure speakers/headphones are connected and working
3. Try adjusting system volume

### Application Won't Start

1. Make sure you're running on Windows 10/11 (for .exe)
2. Try running as administrator (for .exe)
3. Check Windows Defender/antivirus isn't blocking the application (for .exe)
4. Ensure Python is in your system PATH (Linux/macOS)
5. Try running with `python3` instead of `python` on Linux/macOS
6. Verify tkinter is installed (included with official Python distributions)

## Support

For issues or feature requests, please create an issue in the project repository.