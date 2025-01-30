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

## Installation

### Windows

1. Install Python 3.6 or higher from [python.org](https://python.org)
   - During installation, make sure to check "Add Python to PATH"

2. Install Sox (for audio alerts):
   - Download Sox for Windows from [SourceForge](https://sourceforge.net/projects/sox/files/sox/)
   - Add Sox to your system PATH

3. Install required Python packages:
   ```cmd
   pip install word2number
   ```

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

1. Download all the Python files (.py) to a directory
2. Run the application:
   ```
   python timer_app.py
   ```
3. Type `help` to see available commands

### Example Commands

- "set a 5 minute timer for coffee break"
- "start a 25 min pomodoro timer"
- "create 1 hour meeting timer"
- "pause the coffee timer"
- "show all timers"
- "stop meeting timer"

The application will understand your intent and execute the command.

## Offline Use

This application works completely offline. Once installed, no internet connection is required.

## Files Description

- `timer_app.py` - Main application with GUI
- `timer_manager.py` - Timer management logic
- `command_interpreter.py` - Natural language command processing
- `command_parser.py` - Command parsing utilities
- `alert_manager.py` - Sound alert management

## Troubleshooting

### No Sound Alerts

1. Verify Sox is installed:
   - Windows: Run `sox --version` in Command Prompt
   - Linux/macOS: Run `sox --version` in Terminal
2. Check system sound settings
3. The application will fall back to visual alerts if sound is unavailable

### Python Installation Issues

- Ensure Python is in your system PATH
- Try running with `python3` instead of `python` on Linux/macOS
- Verify tkinter is installed (included with official Python distributions)