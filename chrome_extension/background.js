
// Background script for Timer Assistant
const timerManager = new TimerManager();

// Play alarm sound when a timer completes
function playAlertSound() {
  const audio = new Audio('sounds/alert.mp3');
  audio.loop = false;
  audio.volume = 1.0;
  
  // Browser requires user interaction before playing audio
  const playPromise = audio.play();
  
  if (playPromise !== undefined) {
    playPromise
      .then(() => {
        console.log('Alert sound played successfully');
      })
      .catch(error => {
        console.error('Failed to play alert sound:', error);
        // Fallback to notification sound
        chrome.notifications.create('', {
          type: 'basic',
          iconUrl: 'images/icon128.png',
          title: 'Timer Complete',
          message: 'Timer finished!',
          priority: 2,
          silent: false
        });
      });
  }
}

// Listen for alarms (timer completions)
chrome.alarms.onAlarm.addListener((alarm) => {
  // Check if this is a timer alarm
  if (alarm.name.startsWith('timer_')) {
    // Extract timer name from alarm name
    const timerName = alarm.name.split('_')[1];
    
    // Show notification
    chrome.notifications.create(`notification_${timerName}`, {
      type: 'basic',
      iconUrl: 'images/icon128.png',
      title: 'Timer Complete',
      message: `Your "${timerName}" timer has finished!`,
      priority: 2,
      silent: false
    });
    
    // Play sound
    playAlertSound();
  }
});

// Listen for messages from the popup
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
  
  // Save state after any changes
  timerManager.saveTimers();
  return true;
});

// Initialize when extension is installed/updated
chrome.runtime.onInstalled.addListener(() => {
  console.log('Timer Assistant Extension installed');
  // Load any saved timers
  timerManager.loadTimers();
});
