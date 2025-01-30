import threading
import time
import subprocess
from typing import Dict, Optional
import os

class AlertManager:
    def __init__(self):
        self.active_alerts: Dict[str, threading.Thread] = {}
        self.alert_stop_flags: Dict[str, bool] = {}
        self.alert_timeout = 120  # 2 minutes in seconds
        
    def _play_alert(self, timer_name: str):
        """Play a beep sound repeatedly until stopped"""
        while not self.alert_stop_flags.get(timer_name, True):
            # Use sox 'play' command to generate a beep
            try:
                subprocess.run(
                    ['play', '-n', 'synth', '0.1', 'sine', '880', 'vol', '0.3'],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                time.sleep(1)  # Pause between beeps
            except Exception:
                # If sound fails, stop the alert
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
