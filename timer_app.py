import sys
from timer_manager import TimerManager
from command_parser import CommandParser

def main():
    print("Timer Management Application")
    print("Type 'help' for available commands")
    
    timer_manager = TimerManager()
    command_parser = CommandParser()
    
    while True:
        try:
            user_input = input("> ").strip().lower()
            
            if user_input == "exit":
                print("Exiting application...")
                timer_manager.stop_all_timers()
                sys.exit(0)
                
            if user_input == "help":
                command_parser.show_help()
                continue
                
            command = command_parser.parse_command(user_input)
            if command:
                timer_manager.execute_command(command)
            else:
                print("Invalid command format. Type 'help' for available commands.")
                
        except KeyboardInterrupt:
            print("\nExiting application...")
            timer_manager.stop_all_timers()
            sys.exit(0)
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
