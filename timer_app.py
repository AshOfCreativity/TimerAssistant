import tkinter as tk
from tkinter import ttk
import re
from timer_manager import TimerManager
from command_interpreter import CommandInterpreter

class TimerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Timer Assistant")
        self.root.geometry("600x400")

        # Set theme for better appearance
        style = ttk.Style()
        style.theme_use('clam')  # Use 'clam' theme for better cross-platform compatibility

        self.timer_manager = TimerManager()
        self.command_interpreter = CommandInterpreter()

        # Create input frame
        self.input_frame = ttk.Frame(self.root)
        self.input_frame.pack(fill=tk.X, padx=5, pady=5)

        # Create command input with placeholder
        self.command_var = tk.StringVar()
        self.command_entry = ttk.Entry(
            self.input_frame, 
            textvariable=self.command_var,
            font=('Arial', 12)
        )
        self.command_entry.pack(fill=tk.X, expand=True, side=tk.LEFT, padx=(0, 5))
        self.command_entry.bind('<Return>', self.process_command)

        # Create "Enter" button
        self.enter_button = ttk.Button(
            self.input_frame,
            text="Enter",
            command=lambda: self.process_command(None)
        )
        self.enter_button.pack(side=tk.RIGHT)

        # Create output text area with scrollbar
        self.output_frame = ttk.Frame(self.root)
        self.output_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.scrollbar = ttk.Scrollbar(self.output_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.output_text = tk.Text(
            self.output_frame,
            height=15,
            font=('Arial', 10),
            yscrollcommand=self.scrollbar.set
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.output_text.yview)

        # Set up timer manager callback
        self.timer_manager.set_output_callback(self.print_output)

        # Initial help message
        self.show_help()

        # Set focus to entry
        self.command_entry.focus_set()

    def show_help(self):
        help_text = """Welcome to Timer Assistant!
Just type what you want in natural language:

Examples:
- "set a 5 minute timer for coffee break"
- "start a 25 min pomodoro timer"
- "create 1 hour meeting timer"
- "pause the coffee timer"
- "show all timers"
- "stop meeting timer"

The assistant will understand your intent and execute the command.
"""
        self.output_text.delete('1.0', tk.END)
        self.output_text.insert('1.0', help_text)

    def print_output(self, text):
        self.output_text.insert('end', f"{text}\n")
        self.output_text.see('end')  # Auto-scroll to the bottom

    def process_command(self, event=None):
        command_text = self.command_var.get().strip()
        if not command_text:
            return

        self.command_var.set("")  # Clear input

        if command_text.lower() == "help":
            self.show_help()
            return

        if command_text.lower() == "exit":
            self.root.quit()
            return

        # Process command through interpreter
        try:
            result = self.command_interpreter.interpret(command_text)
            if result:
                self.timer_manager.execute_command(result)
                self.print_output(f"Executed: {command_text}")
            else:
                self.print_output("I didn't understand that command. Try rephrasing or type 'help'.")
        except Exception as e:
            self.print_output(f"Error: {str(e)}")

    def run(self):
        # Make sure the window appears on top when started
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.attributes('-topmost', False)
        self.root.mainloop()

if __name__ == "__main__":
    app = TimerApp()
    app.run()