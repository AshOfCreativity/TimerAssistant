import threading
import time
from datetime import datetime, timedelta
from typing import Dict, Optional, Callable

class Timer:
    def __init__(self, name: str, duration: int):
        self.name = name
        self.duration = duration
        self.remaining = duration
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self.paused = False
        self.start_time: Optional[datetime] = None
        self.callback: Optional[Callable[[str], None]] = None

    def format_time(self, seconds: int) -> str:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60

        if hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"

    def run(self):
        self.start_time = datetime.now()
        while self.remaining > 0 and self.running:
            if not self.paused:
                if self.callback:
                    self.callback(f"Timer '{self.name}' - {self.format_time(self.remaining)} remaining")
                time.sleep(1)
                self.remaining -= 1
            else:
                time.sleep(0.1)

        if self.remaining <= 0 and self.running:
            if self.callback:
                self.callback(f"\nTimer '{self.name}' has finished!")

class TimerManager:
    def __init__(self):
        self.timers: Dict[str, Timer] = {}
        self.output_callback = None

    def set_output_callback(self, callback: Callable[[str], None]):
        """Set callback for timer output"""
        self.output_callback = callback

    def _print(self, message: str):
        """Print message using callback if available"""
        if self.output_callback:
            self.output_callback(message)
        else:
            print(message)

    def create_timer(self, name: str, duration: int) -> None:
        if name in self.timers:
            raise ValueError(f"Timer '{name}' already exists")

        timer = Timer(name, duration)
        timer.callback = self._print
        self.timers[name] = timer
        self._print(f"Created timer '{name}' with duration of {timer.format_time(duration)}")

        # Automatically start the timer
        self.start_timer(name)

    def start_timer(self, name: str) -> None:
        if name not in self.timers:
            raise ValueError(f"Timer '{name}' does not exist")

        timer = self.timers[name]
        if timer.running:
            self._print(f"Timer '{name}' is already running")
            return

        timer.running = True
        timer.paused = False
        timer.thread = threading.Thread(target=timer.run)
        timer.thread.daemon = True
        timer.thread.start()
        self._print(f"Started timer '{name}'")

    def pause_timer(self, name: str) -> None:
        if name not in self.timers:
            raise ValueError(f"Timer '{name}' does not exist")

        timer = self.timers[name]
        if not timer.running:
            self._print(f"Timer '{name}' is not running")
            return

        timer.paused = True
        self._print(f"\nPaused timer '{name}' with {timer.format_time(timer.remaining)} remaining")

    def resume_timer(self, name: str) -> None:
        if name not in self.timers:
            raise ValueError(f"Timer '{name}' does not exist")

        timer = self.timers[name]
        if not timer.running:
            self._print(f"Timer '{name}' is not running")
            return

        timer.paused = False
        self._print(f"Resumed timer '{name}' with {timer.format_time(timer.remaining)} remaining")

    def stop_timer(self, name: str) -> None:
        if name not in self.timers:
            raise ValueError(f"Timer '{name}' does not exist")

        timer = self.timers[name]
        timer.running = False
        if timer.thread:
            timer.thread.join(0.1)
        timer.remaining = timer.duration
        self._print(f"Stopped timer '{name}'")

    def delete_timer(self, name: str) -> None:
        if name not in self.timers:
            raise ValueError(f"Timer '{name}' does not exist")

        self.stop_timer(name)
        del self.timers[name]
        self._print(f"Deleted timer '{name}'")

    def list_timers(self) -> None:
        if not self.timers:
            self._print("No timers exist")
            return

        self._print("\nCurrent Timers:")
        self._print("-" * 50)
        for name, timer in self.timers.items():
            status = "Running" if timer.running and not timer.paused else "Paused" if timer.paused else "Stopped"
            self._print(f"Name: {name}")
            self._print(f"Duration: {timer.format_time(timer.duration)}")
            self._print(f"Remaining: {timer.format_time(timer.remaining)}")
            self._print(f"Status: {status}")
            self._print("-" * 50)

    def stop_all_timers(self) -> None:
        for name in list(self.timers.keys()):
            self.stop_timer(name)

    def execute_command(self, command: dict) -> None:
        cmd_type = command["type"]

        if cmd_type == "create":
            self.create_timer(command["name"], command["duration"])
        elif cmd_type == "start":
            self.start_timer(command["name"])
        elif cmd_type == "pause":
            self.pause_timer(command["name"])
        elif cmd_type == "resume":
            self.resume_timer(command["name"])
        elif cmd_type == "stop":
            self.stop_timer(command["name"])
        elif cmd_type == "delete":
            self.delete_timer(command["name"])
        elif cmd_type == "list":
            self.list_timers()