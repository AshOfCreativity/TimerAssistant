from typing import Optional, Dict

class CommandParser:
    def show_help(self):
        help_text = """
Available Commands:
------------------
create <name> <duration> - Create a new timer (e.g., "create pomodoro 25m" or "create break 5m")
                        Duration format: 30s (seconds), 5m (minutes), 2h (hours)
start <name>           - Start a timer
pause <name>          - Pause a running timer
resume <name>         - Resume a paused timer
stop <name>           - Stop a timer
delete <name>         - Delete a timer
list                  - List all timers
help                  - Show this help message
exit                  - Exit the application

Examples:
---------
create pomodoro 25m   - Creates a 25-minute timer named 'pomodoro'
create break 5m       - Creates a 5-minute timer named 'break'
create test 30s       - Creates a 30-second timer named 'test'
create long 2h        - Creates a 2-hour timer named 'long'
start pomodoro        - Starts the pomodoro timer
list                  - Shows all timers and their status
"""
        print(help_text)

    def _parse_duration(self, duration_str: str) -> Optional[int]:
        try:
            if duration_str.endswith('s'):
                return int(duration_str[:-1])
            elif duration_str.endswith('m'):
                return int(duration_str[:-1]) * 60
            elif duration_str.endswith('h'):
                return int(duration_str[:-1]) * 3600
            else:
                try:
                    return int(duration_str)  # Assume seconds if no unit specified
                except ValueError:
                    print("Error: Invalid duration format. Use 30s, 5m, or 2h")
                    return None
        except ValueError:
            print("Error: Duration must be a valid number followed by s, m, or h")
            return None

    def parse_command(self, command_str: str) -> Optional[Dict]:
        parts = command_str.split()
        if not parts:
            return None

        command = parts[0]

        if command == "list":
            return {"type": "list"}

        if len(parts) < 2:
            return None

        name = parts[1]

        if command == "create":
            if len(parts) != 3:
                print("Error: Create command requires a name and duration (e.g., create pomodoro 25m)")
                return None

            duration = self._parse_duration(parts[2])
            if duration is None:
                return None
            if duration <= 0:
                print("Error: Duration must be a positive number")
                return None

            return {"type": "create", "name": name, "duration": duration}

        elif command in ["start", "pause", "resume", "stop", "delete"]:
            return {"type": command, "name": name}

        print(f"Unknown command: {command}")
        return None