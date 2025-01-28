import threading
import time
from datetime import datetime, timedelta
from typing import Dict, Optional

class Timer:
    def __init__(self, name: str, duration: int):
        self.name = name
        self.duration = duration
        self.remaining = duration
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self.paused = False
        self.start_time: Optional[datetime] = None

    def run(self):
        self.start_time = datetime.now()
        while self.remaining > 0 and self.running:
            if not self.paused:
                time.sleep(1)
                self.remaining -= 1
            else:
                time.sleep(0.1)

        if self.remaining <= 0 and self.running:
            print("\a")  # Console bell
            print(f"\nTimer '{self.name}' has finished!")
            print("> ", end="", flush=True)  # Restore prompt

class TimerManager:
    def __init__(self):
        self.timers: Dict[str, Timer] = {}

    def create_timer(self, name: str, duration: int) -> None:
        if name in self.timers:
            raise ValueError(f"Timer '{name}' already exists")

        self.timers[name] = Timer(name, duration)
        print(f"Created timer '{name}' with duration of {duration} seconds")

    def start_timer(self, name: str) -> None:
        if name not in self.timers:
            raise ValueError(f"Timer '{name}' does not exist")

        timer = self.timers[name]
        if timer.running:
            print(f"Timer '{name}' is already running")
            return

        timer.running = True
        timer.paused = False
        timer.thread = threading.Thread(target=timer.run)
        timer.thread.daemon = True
        timer.thread.start()
        print(f"Started timer '{name}'")

    def pause_timer(self, name: str) -> None:
        if name not in self.timers:
            raise ValueError(f"Timer '{name}' does not exist")

        timer = self.timers[name]
        if not timer.running:
            print(f"Timer '{name}' is not running")
            return

        timer.paused = True
        print(f"Paused timer '{name}'")

    def resume_timer(self, name: str) -> None:
        if name not in self.timers:
            raise ValueError(f"Timer '{name}' does not exist")

        timer = self.timers[name]
        if not timer.running:
            print(f"Timer '{name}' is not running")
            return

        timer.paused = False
        print(f"Resumed timer '{name}'")

    def stop_timer(self, name: str) -> None:
        if name not in self.timers:
            raise ValueError(f"Timer '{name}' does not exist")

        timer = self.timers[name]
        timer.running = False
        if timer.thread:
            timer.thread.join(0.1)
        timer.remaining = timer.duration
        print(f"Stopped timer '{name}'")

    def delete_timer(self, name: str) -> None:
        if name not in self.timers:
            raise ValueError(f"Timer '{name}' does not exist")

        self.stop_timer(name)
        del self.timers[name]
        print(f"Deleted timer '{name}'")

    def list_timers(self) -> None:
        if not self.timers:
            print("No timers exist")
            return

        print("\nCurrent Timers:")
        print("-" * 50)
        for name, timer in self.timers.items():
            status = "Running" if timer.running and not timer.paused else "Paused" if timer.paused else "Stopped"
            print(f"Name: {name}")
            print(f"Duration: {timer.duration} seconds")
            print(f"Remaining: {timer.remaining} seconds")
            print(f"Status: {status}")
            print("-" * 50)

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