import tkinter as tk
from tkinter import ttk
import re
from timer_manager import TimerManager
from command_interpreter import CommandInterpreter

class TimerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Timer Assistant")
        self.root.geometry("800x500")

        # Set theme for better appearance
        style = ttk.Style()
        style.theme_use('clam')

        self.timer_manager = TimerManager()
        self.command_interpreter = CommandInterpreter()

        # Create main container with left and right panes
        self.paned_window = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Left pane for input and general output
        self.left_pane = ttk.Frame(self.paned_window)
        self.paned_window.add(self.left_pane, weight=2)

        # Right pane for active timers
        self.right_pane = ttk.Frame(self.paned_window)
        self.paned_window.add(self.right_pane, weight=1)

        # Set up left pane components
        self.setup_left_pane()

        # Set up right pane components
        self.setup_right_pane()

        # Set up timer manager callback
        self.timer_manager.set_output_callback(self.print_output)

        # Initial help message
        self.show_help()

        # Set focus to entry
        self.command_entry.focus_set()

    def setup_left_pane(self):
        # Input frame
        self.input_frame = ttk.Frame(self.left_pane)
        self.input_frame.pack(fill=tk.X, padx=5, pady=5)

        # Command input with placeholder
        self.command_var = tk.StringVar()
        self.command_entry = ttk.Entry(
            self.input_frame, 
            textvariable=self.command_var,
            font=('Arial', 12)
        )
        self.command_entry.pack(fill=tk.X, expand=True, side=tk.LEFT, padx=(0, 5))
        self.command_entry.bind('<Return>', self.process_command)

        # Enter button
        self.enter_button = ttk.Button(
            self.input_frame,
            text="Enter",
            command=lambda: self.process_command(None)
        )
        self.enter_button.pack(side=tk.RIGHT)

        # Output text area with scrollbar
        self.output_frame = ttk.Frame(self.left_pane)
        self.output_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.scrollbar = ttk.Scrollbar(self.output_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.output_text = tk.Text(
            self.output_frame,
            font=('Arial', 10),
            yscrollcommand=self.scrollbar.set
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.output_text.yview)

    def setup_right_pane(self):
        # Active Timers label
        self.timer_label = ttk.Label(
            self.right_pane,
            text="Active Timers",
            font=('Arial', 12, 'bold')
        )
        self.timer_label.pack(pady=5)

        # Frame for active timers
        self.active_timers_frame = ttk.Frame(self.right_pane)
        self.active_timers_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Dictionary to keep track of timer labels
        self.timer_labels = {}

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

    def update_timer_display(self, name: str, time_str: str, status: str):
        """Update or create a timer display in the right pane"""
        if name not in self.timer_labels:
            # Create new timer frame
            timer_frame = ttk.Frame(self.active_timers_frame)
            timer_frame.pack(fill=tk.X, pady=2)

            # Timer name and remaining time
            label = ttk.Label(
                timer_frame,
                font=('Arial', 10),
                anchor='w'
            )
            label.pack(side=tk.LEFT, padx=5)

            self.timer_labels[name] = {
                'frame': timer_frame,
                'label': label
            }

        # Update label text with status icon
        status_icon = "⏸️" if status == "paused" else "⏱️" if status == "running" else "⚠️"
        self.timer_labels[name]['label'].config(
            text=f"{status_icon} {name}: {time_str}"
        )

    def remove_timer_display(self, name: str):
        """Remove a timer display from the right pane"""
        if name in self.timer_labels:
            self.timer_labels[name]['frame'].destroy()
            del self.timer_labels[name]

    def print_output(self, text):
        """Handle output from timer manager"""
        # Check if this is a timer update message
        timer_update = re.match(r'\[(.*?)\]:\s*(.*)', text)
        if timer_update:
            name, info = timer_update.groups()
            if "Complete" in info:
                status = "complete"
                self.update_timer_display(name, "Done!", status)
                self.output_text.insert('end', f"Timer '{name}' completed!\n")
            else:
                status = "running"
                if name in self.timer_labels:
                    # Check if timer is paused
                    timer = self.timer_manager.timers.get(name)
                    if timer and timer.paused:
                        status = "paused"
                self.update_timer_display(name, info, status)
        else:
            self.output_text.insert('end', f"{text}\n")
        self.output_text.see('end')

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