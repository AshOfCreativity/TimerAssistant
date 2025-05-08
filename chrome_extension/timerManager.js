class Timer {
  constructor(name, duration) {
    this.name = name;
    this.duration = duration;
    this.remaining = duration;
    this.running = false;
    this.paused = false;
    this.intervalId = null;
    this.callback = null;
    this.alerting = false;
    this.alarmName = `timer_${name}_${Date.now()}`;
  }

  formatTime(seconds) {
    if (seconds <= 0) return "0m";
    const minutes = Math.floor(seconds / 60);
    return minutes > 0 ? `${minutes}m` : `${seconds}s`;
  }

  start(callback) {
    this.callback = callback;
    this.running = true;
    this.paused = false;
    if (this.intervalId) clearInterval(this.intervalId);
    if (this.callback) this.callback(`[${this.name}]: ${this.formatTime(this.remaining)}`);
    this.intervalId = setInterval(() => {
      if (!this.paused && this.running) {
        this.remaining--;
        if (this.callback) this.callback(`[${this.name}]: ${this.formatTime(this.remaining)}`);
        if (this.remaining <= 0) this.complete();
      }
    }, 1000);
    chrome.alarms.create(this.alarmName, {
      delayInMinutes: this.remaining / 60
    });
  }

  pause() {
    this.paused = true;
    if (this.callback) this.callback(`[${this.name}]: ${this.formatTime(this.remaining)}`);
  }

  resume() {
    this.paused = false;
    if (this.callback) this.callback(`[${this.name}]: ${this.formatTime(this.remaining)}`);
  }

  stop() {
    this.running = false;
    if (this.intervalId) {
      clearInterval(this.intervalId);
      this.intervalId = null;
    }
    // Clear the alarm
    chrome.alarms.clear(this.alarmName);
    this.remaining = this.duration;
  }

  complete() {
    this.stop();
    this.alerting = true;
    if (this.callback) this.callback(`[${this.name}]: Complete!`);
    // Show a notification
    chrome.notifications.create(`notification_${this.name}`, {
      type: 'basic',
      iconUrl: 'images/icon128.png',
      title: 'Timer Complete',
      message: `Your "${this.name}" timer has finished!`,
      priority: 2,
      silent: false
    });
    // Send message to background script to play sound
    chrome.runtime.sendMessage({ action: 'playAlert' });
  }
}

// TimerManager class using Timer
class TimerManager {
  constructor() {
    this.timers = {};
    this.outputCallback = null;
  }

  setOutputCallback(callback) {
    this.outputCallback = callback;
  }

  _print(message) {
    if (this.outputCallback) this.outputCallback(message);
    else console.log(message);
  }

  createTimer(name, duration) {
    if (this.timers[name]) {
      if (this.timers[name].alerting) {
        this.timers[name].alerting = false;
        this.timers[name].duration = duration;
        this.timers[name].remaining = duration;
        this.timers[name].running = true;
        this.timers[name].paused = false;
        this._print(`Refreshed timer '${name}'`);
        this.startTimer(name);
        return;
      }
      throw new Error(`Timer '${name}' already exists`);
    }
    const timer = new Timer(name, duration);
    this.timers[name] = timer;
    this._print(`Created timer '${name}'`);
    this.startTimer(name);
  }

  startTimer(name) {
    const timer = this.timers[name];
    if (!timer) throw new Error(`Timer '${name}' does not exist`);
    timer.start((message) => this._print(message));
  }

  pauseTimer(name) {
    if (!this.timers[name]) {
      throw new Error(`Timer '${name}' does not exist`);
    }

    const timer = this.timers[name];
    if (!timer.running) {
      this._print(`Timer '${name}' is not running`);
      return;
    }

    timer.pause();
    this._print(`Paused timer '${name}'`);
  }

  resumeTimer(name) {
    if (!this.timers[name]) {
      throw new Error(`Timer '${name}' does not exist`);
    }

    const timer = this.timers[name];
    if (!timer.running) {
      this._print(`Timer '${name}' is not running`);
      return;
    }

    if (!timer.paused) {
      this._print(`Timer '${name}' is already running`);
      return;
    }

    timer.resume();
    this._print(`Resumed timer '${name}'`);
  }

  stopTimer(name) {
    if (!this.timers[name]) {
      throw new Error(`Timer '${name}' does not exist`);
    }

    const timer = this.timers[name];
    timer.stop();
    this._print(`Stopped timer '${name}'`);
    this._print(`[${name}]: Complete!`);
  }

  deleteTimer(name) {
    if (!this.timers[name]) {
      throw new Error(`Timer '${name}' does not exist`);
    }

    this.stopTimer(name);
    delete this.timers[name];
    this._print(`Deleted timer '${name}'`);
    chrome.runtime.sendMessage({
      action: 'deleteTimer',
      name: name
    });
  }

  listTimers() {
    const timerCount = Object.keys(this.timers).length;
    if (timerCount === 0) {
      this._print("No active timers");
      return;
    }

    this._print(`Active timers (${timerCount}):`);
    for (const [name, timer] of Object.entries(this.timers)) {
      const status = timer.paused ? "paused" : "running";
      this._print(`[${name}]: ${timer.formatTime(timer.remaining)} (${status})`);
    }
  }

  stopAllTimers() {
    Object.keys(this.timers).forEach(name => {
      this.stopTimer(name);
    });
  }

  executeCommand(command) {
    try {
      const cmdType = command.type;

      switch (cmdType) {
        case "create":
          this.createTimer(command.name, command.duration);
          break;
        case "start":
          this.startTimer(command.name);
          break;
        case "pause":
          this.pauseTimer(command.name);
          break;
        case "resume":
          this.resumeTimer(command.name);
          break;
        case "stop":
          this.stopTimer(command.name);
          break;
        case "delete":
          this.deleteTimer(command.name);
          break;
        case "list":
          this.listTimers();
          break;
        default:
          this._print(`Unknown command type: ${cmdType}`);
      }
    } catch (error) {
      this._print(`Error: ${error.message}`);
    }
  }

  saveTimers() {
    const timersData = {};

    for (const [name, timer] of Object.entries(this.timers)) {
      timersData[name] = {
        name: timer.name,
        duration: timer.duration,
        remaining: timer.remaining,
        running: timer.running,
        paused: timer.paused,
        alerting: timer.alerting
      };
    }

    chrome.storage.local.set({ 'timers': timersData });
  }

  loadTimers(callback) {
    chrome.storage.local.get('timers', (result) => {
      if (result.timers) {
        for (const [name, timerData] of Object.entries(result.timers)) {
          const timer = new Timer(timerData.name, timerData.duration);
          timer.remaining = timerData.remaining;
          timer.running = timerData.running;
          timer.paused = timerData.paused;
          timer.alerting = timerData.alerting;

          this.timers[name] = timer;

          if (timer.running && !timer.paused && !timer.alerting) {
            timer.start((message) => {
              this._print(message);
            });
          }
        }
      }

      if (callback) callback();
    });
  }
}

window.TimerManager = TimerManager;
window.Timer = Timer;