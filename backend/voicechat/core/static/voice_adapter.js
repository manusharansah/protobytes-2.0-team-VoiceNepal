(function () {
  // Map incoming lang codes ('en-US', 'ne-NP', 'en', 'ne') to Web Speech values
  function normalizeLangCode(langCode) {
    if (!langCode) return 'en-US';
    if (langCode.startsWith('ne')) return 'ne-NP';
    if (langCode.startsWith('en')) return 'en-US';
    return langCode;
  }

  // Start speech-to-text, modeled after startDictation() in core/templates/core/index.html
  async function startSpeechToText(onTextChunk, onEnd, onError, langCode) {
    try {
      if (!window.hasOwnProperty('webkitSpeechRecognition')) {
        const err = new Error('Speech recognition not supported in this browser.');
        if (onError) onError(err);
        return null;
      }

      const recognition = new webkitSpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = normalizeLangCode(langCode);

      recognition.onresult = function (e) {
        const transcript = e.results[0][0].transcript;
        if (onTextChunk) onTextChunk(transcript, e);
        recognition.stop();
        if (onEnd) onEnd();
      };

      recognition.onerror = function (e) {
        recognition.stop();
        if (onError) onError(e);
        if (onEnd) onEnd();
      };

      recognition.start();
      return recognition;
    } catch (e) {
      if (onError) onError(e);
      if (onEnd) onEnd();
      return null;
    }
  }

  // Stop recognition if active
  function stopSpeechToText(recognitionInstance) {
    if (recognitionInstance && typeof recognitionInstance.stop === 'function') {
      recognitionInstance.stop();
    }
  }

  // Text-to-speech, modeled after playbackText() in core/templates/core/index.html
  function sanitizeSpeechText(text) {
    if (!text) return '';

    return String(text)
      .replace(/```[\s\S]*?```/g, ' ')
      .replace(/`{1,3}/g, ' ')
      .replace(/\[(.*?)\]\((.*?)\)/g, '$1')
      .replace(/https?:\/\/\S+|www\.\S+/g, ' ')
      .replace(/^\s*[-+*]\s+/gm, '')
      .replace(/[#*_~>|]/g, ' ')
      .replace(/_/g, ' ')
      .replace(/[^\w\s.,!?;:'"()\-\u0900-\u097F।]/g, ' ')
      .replace(/\s+/g, ' ')
      .trim();
  }

  function speakText(text, langCode) {
    const cleanText = sanitizeSpeechText(text);
    if (!cleanText) return;

    if (!('speechSynthesis' in window)) {
      return;
    }

    // Cancel any ongoing speech
    window.speechSynthesis.cancel();

    let voices = window.speechSynthesis.getVoices();
    let femaleVoice = null;

    // Common female indicators in voice names
    const femaleVoiceKeywords = [
      'female',
      'woman',
      'girl',
      'samantha',
      'karen',
      'monica',
      'daniel',
      'kate',
      'siri',
      'alexa',
      'cortana',
    ];

    // Try to find a female voice by name
    for (let voice of voices) {
      const voiceName = voice.name.toLowerCase();
      if (femaleVoiceKeywords.some((keyword) => voiceName.includes(keyword))) {
        femaleVoice = voice;
        break;
      }
    }

    // If not found, try some known female voices
    if (!femaleVoice) {
      const preferredFemaleVoices = [
        'Microsoft Zira Desktop',
        'Microsoft Hazel Desktop',
        'Google US English Female',
        'Samantha',
        'Karen',
        'Tessa',
        'Susan',
        'Moira',
      ];

      for (let preferredName of preferredFemaleVoices) {
        femaleVoice = voices.find((voice) => voice.name.includes(preferredName));
        if (femaleVoice) break;
      }
    }

    // Fallback: any female-ish English voice
    if (!femaleVoice) {
      femaleVoice = voices.find(
        (voice) =>
          voice.lang.startsWith('en') &&
          (voice.name.toLowerCase().includes('female') ||
            voice.name.toLowerCase().includes('woman') ||
            voice.name.toLowerCase().includes('girl'))
      );
    }

    // Last resort: match language, then English
    const normLang = normalizeLangCode(langCode);
    const langPrefix = normLang.startsWith('ne') ? 'ne' : 'en';
    if (!femaleVoice) {
      femaleVoice = voices.find((voice) => voice.lang.startsWith(langPrefix));
    }
    if (!femaleVoice) {
      femaleVoice = voices.find((voice) => voice.lang.startsWith('en'));
    }

    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.lang = normLang;

    if (femaleVoice) {
      utterance.voice = femaleVoice;
    }

    // Slightly tuned settings for clarity
    utterance.rate = 0.9;
    utterance.pitch = 1.1;
    utterance.volume = 1.0;

    window.speechSynthesis.speak(utterance);
  }

  // Expose a single global object for other frontends (like SajiloSewa)
  window.voiceSearcher = {
    startSpeechToText,
    stopSpeechToText,
    speakText,
  };
})();

