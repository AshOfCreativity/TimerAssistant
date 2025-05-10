document.addEventListener('DOMContentLoaded', function() {
  // Initialize components
  const commandInput = document.getElementById('command-input');
  const submitBtn = document.getElementById('submit-btn');
  const outputText = document.getElementById('output-text');
  const activeTimersContainer = document.getElementById('active-timers');

  // Initialize the timer manager and command interpreter
  const timerManager = new TimerManager();
  const commandInterpreter = new CommandInterpreter();

  // Function to sync with background timer state
  function syncWithBackground() {
    chrome.runtime.sendMessage({ action: 'getTimers' }, function(response) {
      if (response && response.timers) {
        Object.entries(response.timers).forEach(function([name, timer]) {
          updateTimerDisplay(name, timer.formatTime(timer.remaining), 
            timer.paused ? "paused" : "running");
        });
      }
    });
  }

  // Set up message handling for timer updates
  chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.type === 'timerUpdate') {
      updateTimerDisplay(message.name, message.timeStr, message.status);
    }
  });

  // Process commands through background
  function processCommand(command) {
    chrome.runtime.sendMessage({
      action: 'createTimer',
      name: command.name,
      duration: command.duration
    });
  }

  // Sync with background state when popup opens
  syncWithBackground();

  // Set up the output display
  function appendOutput(message) {
    // Check if this is a timer update message
    const timerUpdateMatch = message.match(/\[(.*?)\]:\s*(.*)/);

    if (timerUpdateMatch) {
      const [_, name, info] = timerUpdateMatch;

      if (info.includes("Complete")) {
        updateTimerDisplay(name, "Done!", "complete");
        appendOutput(`Timer '${name}' completed!`);
      } else {
        const status = name in timerManager.timers && 
                       timerManager.timers[name].paused ? "paused" : "running";
        updateTimerDisplay(name, info, status);
      }
    } else {
      // Regular output message
      appendOutput(message);
    }
  }

  // Function to append text to the output area
  function appendOutput(text) {
    outputText.innerHTML += text + '<br>';
    outputText.scrollTop = outputText.scrollHeight;
  }

  // Function to show the help message
  function showHelp() {
    outputText.innerHTML = `Welcome to Timer Assistant!<br>
Just type what you want in natural language:<br>
<br>
Examples:<br>
- "set a 5 minute timer for coffee break"<br>
- "start a 25 min pomodoro timer"<br>
- "create 1 hour meeting timer"<br>
- "pause the coffee timer"<br>
- "show all timers"<br>
- "stop meeting timer"<br>
<br>
The assistant will understand your intent and execute the command.`;
  }

  // Function to update or create timer display in the UI
  function updateTimerDisplay(name, timeStr, status) {
    let timerElement = document.getElementById(`timer-${name}`);

    // Create new timer element if it doesn't exist
    if (!timerElement) {
      timerElement = document.createElement('div');
      timerElement.id = `timer-${name}`;
      timerElement.className = `timer-item timer-${status}`;

      const nameSpan = document.createElement('span');
      nameSpan.className = 'timer-name';
      nameSpan.textContent = name;

      const timeSpan = document.createElement('span');
      timeSpan.className = 'timer-time';
      timeSpan.id = `timer-time-${name}`;

      const controlsDiv = document.createElement('div');
      controlsDiv.className = 'timer-controls';

      // Pause/Resume button
      const pauseResumeBtn = document.createElement('button');
      pauseResumeBtn.className = 'timer-btn';
      pauseResumeBtn.id = `timer-pause-${name}`;
      pauseResumeBtn.innerHTML = '⏸️';
      pauseResumeBtn.title = 'Pause/Resume';
      pauseResumeBtn.addEventListener('click', function() {
        if (timerManager.timers[name].paused) {
          timerManager.resumeTimer(name);
        } else {
          timerManager.pauseTimer(name);
        }
      });

      // Stop button
      const stopBtn = document.createElement('button');
      stopBtn.className = 'timer-btn';
      stopBtn.innerHTML = '⏹️';
      stopBtn.title = 'Stop';
      stopBtn.addEventListener('click', function() {
        timerManager.stopTimer(name);
      });

      // Delete button
      const deleteBtn = document.createElement('button');
      deleteBtn.className = 'timer-btn';
      deleteBtn.innerHTML = '🗑️';
      deleteBtn.title = 'Delete';
      deleteBtn.addEventListener('click', function() {
        timerManager.deleteTimer(name);
        removeTimerDisplay(name);
      });

      controlsDiv.appendChild(pauseResumeBtn);
      controlsDiv.appendChild(stopBtn);
      controlsDiv.appendChild(deleteBtn);

      timerElement.appendChild(nameSpan);
      timerElement.appendChild(timeSpan);
      timerElement.appendChild(controlsDiv);

      activeTimersContainer.appendChild(timerElement);
    } else {
      // Update existing timer element
      timerElement.className = `timer-item timer-${status}`;
    }

    // Update the time display
    const timeElement = document.getElementById(`timer-time-${name}`);
    if (timeElement) {
      const statusIcon = status === "paused" ? "⏸️" : 
                         status === "running" ? "⏱️" : "✅";
      timeElement.textContent = `${statusIcon} ${timeStr}`;
    }

    // Update pause/resume button text if it exists
    const pauseResumeBtn = document.getElementById(`timer-pause-${name}`);
    if (pauseResumeBtn) {
      pauseResumeBtn.innerHTML = status === "paused" ? "▶️" : "⏸️";
    }
  }

  // Function to remove a timer display
  function removeTimerDisplay(name) {
    const timerElement = document.getElementById(`timer-${name}`);
    if (timerElement) {
      timerElement.remove();
    }
  }

  // Process the command
  function processCommand() {
    const commandText = commandInput.value.trim();
    if (!commandText) return;

    // Clear the input field
    commandInput.value = "";

    // Check for help command
    if (commandText.toLowerCase() === "help") {
      showHelp();
      return;
    }

    // Process command through interpreter
    try {
      const result = commandInterpreter.interpret(commandText);
      if (result) {
        timerManager.executeCommand(result);
        appendOutput(`Executed: ${commandText}`);

        // Save timers to storage
        timerManager.saveTimers();
      } else {
        appendOutput("I didn't understand that command. Try rephrasing or type 'help'.");
      }
    } catch (error) {
      appendOutput(`Error: ${error.message}`);
    }
  }

  // Set up event listeners
  submitBtn.addEventListener('click', processCommand);
  commandInput.addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
      processCommand();
    }
  });

  // Load timers from storage when popup opens
  timerManager.loadTimers(function() {
    // Display any existing timers
    for (const [name, timer] of Object.entries(timerManager.timers)) {
      const status = timer.paused ? "paused" : 
                    timer.alerting ? "complete" : "running";
      updateTimerDisplay(name, timer.formatTime(timer.remaining), status);
    }
  });

  // Initial help message
  showHelp();

  // Set focus to input
  commandInput.focus();
});