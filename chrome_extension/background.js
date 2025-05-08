
// Background script for Timer Assistant
const timerManager = new TimerManager();

// Sound handling with fallbacks
class SoundPlayer {
  constructor() {
    this.audioContext = null;
    this.soundBuffer = null;
    this.fallbackAudio = null;
    this.initializeAudio();
  }

  async initializeAudio() {
    try {
      // Try Web Audio API first
      this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
      const response = await fetch('sounds/alert.mp3');
      const arrayBuffer = await response.arrayBuffer();
      this.soundBuffer = await this.audioContext.decodeAudioData(arrayBuffer);
    } catch (e) {
      console.log('Web Audio API failed, using fallback:', e);
      // Fallback to HTML5 Audio
      this.fallbackAudio = new Audio('sounds/alert.mp3');
    }
  }

  async play() {
    try {
      if (this.audioContext && this.soundBuffer) {
        const source = this.audioContext.createBufferSource();
        source.buffer = this.soundBuffer;
        source.connect(this.audioContext.destination);
        source.start(0);
        return true;
      } else if (this.fallbackAudio) {
        await this.fallbackAudio.play();
        return true;
      }
    } catch (e) {
      console.error('Sound playback failed:', e);
      return false;
    }
    return false;
  }
}

const soundPlayer = new SoundPlayer();

// Play alarm sound with fallbacks
async function playAlertSound() {
  const soundSuccess = await soundPlayer.play();
  
  if (!soundSuccess) {
    // Final fallback - system notification with sound
    chrome.notifications.create('', {
      type: 'basic',
      iconUrl: 'images/icon128.png',
      title: 'Timer Complete',
      message: 'Timer finished!',
      priority: 2,
      silent: false
    });
  }
}

// Ensure extension stays active
chrome.runtime.onStartup.addListener(() => {
  timerManager.loadTimers();
});

chrome.runtime.onInstalled.addListener(() => {
  timerManager.loadTimers();
});

// Listen for alarms
chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name.startsWith('timer_')) {
    const timerName = alarm.name.split('_')[1];
    
    chrome.notifications.create(`notification_${timerName}`, {
      type: 'basic',
      iconUrl: 'images/icon128.png',
      title: 'Timer Complete',
      message: `Your "${timerName}" timer has finished!`,
      priority: 2,
      requireInteraction: true,
      silent: false
    });
    
    playAlertSound();
  }
});

// Message handling
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  switch (message.action) {
    case 'createTimer':
      timerManager.createTimer(message.name, message.duration);
      break;
    case 'getTimers':
      sendResponse({ timers: timerManager.timers });
      break;
    case 'pauseTimer':
      timerManager.pauseTimer(message.name);
      break;
    case 'resumeTimer':
      timerManager.resumeTimer(message.name);
      break;
    case 'stopTimer':
      timerManager.stopTimer(message.name);
      break;
    case 'deleteTimer':
      timerManager.deleteTimer(message.name);
      break;
    case 'playAlert':
      playAlertSound();
      break;
  }
  
  timerManager.saveTimers();
  return true;
});

// Keep alive
setInterval(() => {
  chrome.runtime.getPlatformInfo(() => {
    if (chrome.runtime.lastError) {
      console.log('Keeping extension alive');
    }
  });
}, 20000);
