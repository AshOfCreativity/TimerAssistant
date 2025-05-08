// Background script for Timer Assistant

// Play alarm sound when a timer completes
function playAlertSound() {
  const audio = new Audio('sounds/alert.mp3');
  audio.loop = false;
  audio.play().catch(error => {
    console.error('Failed to play alert sound:', error);
  });
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

// Listen for notification clicks
chrome.notifications.onClicked.addListener((notificationId) => {
  // If it's a timer notification, open the popup
  if (notificationId.startsWith('notification_')) {
    chrome.action.openPopup();
  }
});

// Listen for messages from the popup
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'playAlert') {
    playAlertSound();
    sendResponse({ success: true });
  } else if (message.action === 'stopAlert') {
    // Stop alert sound if implemented
    sendResponse({ success: true });
  } else if (message.action === 'deleteTimer') {
    // Clear any alarms for this timer
    chrome.alarms.getAll((alarms) => {
      alarms.forEach((alarm) => {
        if (alarm.name.includes(message.name)) {
          chrome.alarms.clear(alarm.name);
        }
      });
    });
    sendResponse({ success: true });
  }
  
  return true; // Indicate we will send a response asynchronously
});

// Initialize when extension is installed/updated
chrome.runtime.onInstalled.addListener(() => {
  console.log('Timer Assistant Extension installed');
});