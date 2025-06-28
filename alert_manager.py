import threading
import time
import subprocess
from typing import Dict, Optional
import os

try:
    import winsound
    WINSOUND_AVAILABLE = True
except ImportError:
    WINSOUND_AVAILABLE = False

class AlertManager:
    def __init__(self):
        self.active_alerts: Dict[str, threading.Thread] = {}
        self.alert_stop_flags: Dict[str, bool] = {}
        self.alert_timeout = 120  # 2 minutes in seconds
        self.volume = 100  # Volume percentage (1-100)
        self.beep_frequency = 880  # Hz
        self.beep_duration = 500  # milliseconds
        self.beep_interval = 1.0  # seconds between beeps

    def _play_alert(self, timer_name: str):
        """Play a beep sound repeatedly until stopped"""
        while not self.alert_stop_flags.get(timer_name, True):
            try:
                if WINSOUND_AVAILABLE:
                    # Use Windows beep with configurable settings
                    winsound.Beep(self.beep_frequency, self.beep_duration)
                else:
                    # Fallback for non-Windows systems
                    print(f"\a")  # ASCII bell
                time.sleep(self.beep_interval)
            except Exception as e:
                print(f"Error playing alert: {str(e)}")
                # If sound fails, try a simple print
                print(f"\a\nTimer {timer_name} completed!")  # \a is ASCII bell
                break

    def start_alert(self, timer_name: str):
        """Start a new alert for a timer"""
        # Stop existing alert if any
        self.stop_alert(timer_name)

        # Set up new alert
        self.alert_stop_flags[timer_name] = False
        alert_thread = threading.Thread(
            target=self._alert_with_timeout,
            args=(timer_name,)
        )
        alert_thread.daemon = True
        self.active_alerts[timer_name] = alert_thread
        alert_thread.start()

    def _alert_with_timeout(self, timer_name: str):
        """Run alert with 2-minute timeout"""
        start_time = time.time()
        self._play_alert(timer_name)

        # Stop if 2 minutes have passed
        if time.time() - start_time >= self.alert_timeout:
            self.stop_alert(timer_name)

    def stop_alert(self, timer_name: str):
        """Stop an active alert"""
        if timer_name in self.alert_stop_flags:
            self.alert_stop_flags[timer_name] = True
            if timer_name in self.active_alerts:
                self.active_alerts[timer_name].join(0.1)
                del self.active_alerts[timer_name]
            del self.alert_stop_flags[timer_name]

    def stop_all_alerts(self):
        """Stop all active alerts"""
        for timer_name in list(self.active_alerts.keys()):
            self.stop_alert(timer_name)
    
    def set_audio_settings(self, frequency=None, duration=None, interval=None):
        """Update audio settings for notifications"""
        if frequency is not None:
            self.beep_frequency = max(37, min(32767, int(frequency)))  # Windows beep limits
        if duration is not None:
            self.beep_duration = max(10, min(5000, int(duration)))  # Reasonable duration limits
        if interval is not None:
            self.beep_interval = max(0.1, min(10.0, float(interval)))  # Reasonable interval limits
    
    def get_audio_settings(self):
        """Get current audio settings"""
        return {
            'frequency': self.beep_frequency,
            'duration': self.beep_duration,
            'interval': self.beep_interval
        }