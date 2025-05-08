class CommandInterpreter {
  constructor() {
    // Common time-related words and their multipliers (in seconds)
    this.timeMultipliers = {
      'second': 1, 'seconds': 1, 'sec': 1, 'secs': 1, 's': 1,
      'minute': 60, 'minutes': 60, 'min': 60, 'mins': 60, 'm': 60,
      'hour': 3600, 'hours': 3600, 'hr': 3600, 'hrs': 3600, 'h': 3600
    };

    // Command type indicators with variations
    this.createIndicators = new Set(['set', 'create', 'make', 'start', 'begin', 'add', 'new']);
    this.pauseIndicators = new Set(['pause', 'hold', 'wait', 'suspend', 'freeze']);
    this.resumeIndicators = new Set(['resume', 'continue', 'unpause', 'start again', 'unfreeze']);
    this.stopIndicators = new Set(['stop', 'end', 'cancel', 'delete', 'remove', 'clear']);
    this.listIndicators = new Set(['list', 'show', 'display', 'view', 'what', 'status']);

    // Maps for word-to-number conversion (simplified version of word2number)
    this.wordToNumberMap = {
      'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
      'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
      'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14, 'fifteen': 15,
      'sixteen': 16, 'seventeen': 17, 'eighteen': 18, 'nineteen': 19, 'twenty': 20,
      'thirty': 30, 'forty': 40, 'fifty': 50, 'sixty': 60,
      'seventy': 70, 'eighty': 80, 'ninety': 90
    };
  }

  // Convert word numbers to actual numbers (simplified version)
  wordToNumber(word) {
    return this.wordToNumberMap[word.toLowerCase()] || null;
  }

  _extractDuration(text) {
    text = text.toLowerCase().trim();
    let totalSeconds = 0;
    let foundTime = false;

    // Handle combined formats first (e.g., "1 hour and 30 minutes", "1h30m")
    const timePartsRegex = /(\d+)\s*([hms]|hour|minute|second|hr|min|sec)s?\b/g;
    let match;
    
    while ((match = timePartsRegex.exec(text)) !== null) {
      const [_, value, unit] = match;
      try {
        const number = parseInt(value);
        if (unit === 'h' || unit === 'hour' || unit === 'hr') {
          totalSeconds += number * 3600;
        } else if (unit === 'm' || unit === 'minute' || unit === 'min') {
          totalSeconds += number * 60;
        } else if (unit === 's' || unit === 'second' || unit === 'sec') {
          totalSeconds += number;
        }
        foundTime = true;
      } catch (e) {
        continue;
      }
    }

    // Try numeric followed by time unit format (e.g., "5 minutes", "5min")
    if (!foundTime) {
      for (const [unit, multiplier] of Object.entries(this.timeMultipliers)) {
        const regex = new RegExp(`(\\d+)\\s*${unit}`, 'g');
        while ((match = regex.exec(text)) !== null) {
          try {
            totalSeconds += parseInt(match[1]) * multiplier;
            foundTime = true;
          } catch (e) {
            continue;
          }
        }
      }
    }

    // Try word numbers (e.g., "five minutes")
    if (!foundTime) {
      for (const [unit, multiplier] of Object.entries(this.timeMultipliers)) {
        const regex = new RegExp(`([a-zA-Z-]+)\\s*${unit}`, 'g');
        while ((match = regex.exec(text)) !== null) {
          try {
            const wordNumber = this.wordToNumber(match[1]);
            if (wordNumber) {
              totalSeconds += wordNumber * multiplier;
              foundTime = true;
            }
          } catch (e) {
            continue;
          }
        }
      }
    }

    // Try standalone numbers (assume minutes if no unit specified)
    if (!foundTime) {
      const numMatch = text.match(/\b(\d+)\b/);
      if (numMatch) {
        try {
          totalSeconds = parseInt(numMatch[1]) * 60;  // Assume minutes
          foundTime = true;
        } catch (e) {
          // Ignore parsing errors
        }
      }
    }

    return foundTime ? totalSeconds : null;
  }

  _extractTimerName(text, durationText) {
    // Remove duration part from text
    text = text.replace(durationText, '').trim();

    // Look for words after "for" or "called" or "named"
    for (const prefix of ['for', 'called', 'named', 'label']) {
      if (text.includes(` ${prefix} `)) {
        let name = text.split(` ${prefix} `)[1].trim();
        // Remove articles and timer word
        name = name.replace(/^(the|a|an)\s+/, '');
        name = name.replace('timer', '').trim();
        if (name) {
          return name;
        }
      }
    }

    // Look for words that could be a name (excluding command words and time units)
    const words = text.toLowerCase().split(/\s+/);
    const excludeWords = new Set([
      ...Object.keys(this.timeMultipliers),
      ...Array.from(this.createIndicators),
      ...Array.from(this.pauseIndicators),
      ...Array.from(this.resumeIndicators),
      ...Array.from(this.stopIndicators),
      ...Array.from(this.listIndicators),
      'a', 'an', 'the', 'timer', 'for', 'called', 'named', 'set'
    ]);

    const potentialNames = words.filter(w => !excludeWords.has(w));
    if (potentialNames.length > 0) {
      return potentialNames.join(' ');
    }

    // Default to "timer" if no name found
    return "timer";
  }

  interpret(text) {
    text = text.toLowerCase().trim();

    // Check for list command
    if (Array.from(this.listIndicators).some(indicator => text.includes(indicator))) {
      return { type: "list" };
    }

    // Check for pause/resume/stop commands
    const commandTypes = [
      { type: "pause", indicators: this.pauseIndicators },
      { type: "resume", indicators: this.resumeIndicators },
      { type: "stop", indicators: this.stopIndicators }
    ];

    for (const { type, indicators } of commandTypes) {
      for (const indicator of indicators) {
        if (text.includes(indicator)) {
          // Extract timer name (everything after the command word)
          let name = text.split(indicator)[1].trim();
          name = name.replace(/^(the|a|an)\s+/, '');  // Remove leading "the" or "a"
          name = name.replace('timer', '').trim();  // Remove "timer"
          return { type, name: name || "timer" };
        }
      }
    }

    // Handle create/start command
    const duration = this._extractDuration(text);
    if (duration) {
      // Find the text that contains the duration
      let durationText = text;  // Default to full text if we can't isolate duration part

      // Try to find the exact duration text that matched
      for (const unit of Object.keys(this.timeMultipliers)) {
        if (text.includes(unit)) {
          // Find the number (word or digit) before the unit
          const match = text.match(new RegExp(`(\\d+|\\w+)\\s*${unit}`));
          if (match) {
            durationText = match[0];
            break;
          }
        }
      }

      const name = this._extractTimerName(text, durationText);
      return { type: "create", name, duration };
    }

    return null;
  }
}

// Make it accessible globally
window.CommandInterpreter = CommandInterpreter;