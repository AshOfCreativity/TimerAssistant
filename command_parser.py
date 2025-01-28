class CommandParser:
    def show_help(self):
        help_text = """
Available Commands:
------------------
create <name> <seconds> - Create a new timer
start <name>           - Start a timer
pause <name>           - Pause a running timer
resume <name>          - Resume a paused timer
stop <name>           - Stop a timer
delete <name>         - Delete a timer
list                  - List all timers
help                  - Show this help message
exit                  - Exit the application

Examples:
---------
create pomodoro 1500  - Creates a 25-minute timer named 'pomodoro'
start pomodoro        - Starts the pomodoro timer
list                  - Shows all timers and their status
"""
        print(help_text)

    def parse_command(self, command_str: str) -> dict:
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
                print("Error: Create command requires a name and duration in seconds")
                return None
            try:
                duration = int(parts[2])
                if duration <= 0:
                    print("Error: Duration must be a positive number")
                    return None
                return {"type": "create", "name": name, "duration": duration}
            except ValueError:
                print("Error: Duration must be a valid number")
                return None
                
        elif command in ["start", "pause", "resume", "stop", "delete"]:
            return {"type": command, "name": name}
            
        print(f"Unknown command: {command}")
        return None
