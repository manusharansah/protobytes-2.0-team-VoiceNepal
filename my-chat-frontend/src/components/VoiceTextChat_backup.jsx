import React, { useState, useRef, useEffect } from 'react';
import { Mic, MicOff, Send, Volume2, Loader2, X } from 'lucide-react';

const VoiceTextChat = () => {
  const [inputText, setInputText] = useState('');
  const [messages, setMessages] = useState([]);
  const [isRecording, setIsRecording] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [inputMode, setInputMode] = useState(null);
  const [interimTranscript, setInterimTranscript] = useState('');
  const [language, setLanguage] = useState('en'); // 'en' or 'ne'
  
  const recognitionRef = useRef(null);
  const messagesEndRef = useRef(null);
  const audioRef = useRef(null);

  // Initialize Speech Recognition
  useEffect(() => {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = false;
      recognitionRef.current.interimResults = true;
      recognitionRef.current.lang = language === 'ne' ? 'ne-NP' : 'en-US';

      recognitionRef.current.onresult = (event) => {
        let interim = '';
        let final = '';

        for (let i = event.resultIndex; i < event.results.length; i++) {
          const transcript = event.results[i][0].transcript;
          if (event.results[i].isFinal) {
            final += transcript;
          } else {
            interim += transcript;
          }
        }

        if (final) {
          setInputText(final);
          setInterimTranscript('');
        } else {
          setInterimTranscript(interim);
        }
      };

      recognitionRef.current.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        setIsRecording(false);
        setInterimTranscript('');
        
        if (event.error === 'no-speech') {
          alert('No speech detected. Please try again.');
        } else if (event.error === 'not-allowed') {
          alert('Microphone access denied. Please enable microphone permissions.');
        }
      };

      recognitionRef.current.onend = () => {
        setIsRecording(false);
        setInterimTranscript('');
        
        if (inputText.trim()) {
          setTimeout(() => {
            sendMessage(inputText);
          }, 100);
        }
      };
    }

    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
    };
  }, [inputText, language]);

  // Auto-scroll
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Update recognition language when language changes
  useEffect(() => {
    if (recognitionRef.current) {
      recognitionRef.current.lang = language === 'ne' ? 'ne-NP' : 'en-US';
    }
  }, [language]);

  // Start recording
  const startRecording = () => {
    if (!recognitionRef.current) {
      alert('Speech recognition is not supported in your browser. Please use Chrome or Edge.');
      return;
    }

    setInputText('');
    setInterimTranscript('');
    setInputMode('voice');
    setIsRecording(true);
    
    try {
      recognitionRef.current.start();
    } catch (error) {
      console.error('Error starting recognition:', error);
      setIsRecording(false);
    }
  };

  // Stop recording
  const stopRecording = () => {
    if (recognitionRef.current && isRecording) {
      recognitionRef.current.stop();
    }
  };

  // Send message to Django backend
  const sendMessage = async (text) => {
    if (!text.trim()) {
      setIsLoading(false);
      setInputMode(null);
      return;
    }

    const currentMode = inputMode || 'text';
    
    // Add user message
    setMessages(prev => [...prev, {
      type: 'user',
      content: text,
      mode: currentMode,
      timestamp: new Date()
    }]);

    setInputText('');
    setIsLoading(true);

    try {
      // Update this URL to match your Django server
      const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      
      const response = await fetch(`${API_URL}/api/chat/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          text: text,
          language: language  // Send language preference
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      // Convert base64 audio to playable blob URL
      const audioBlob = base64ToBlob(data.audio_base64, 'audio/mp3');
      const audioBlobUrl = URL.createObjectURL(audioBlob);
      
      // Add assistant response
      setMessages(prev => [...prev, {
        type: 'assistant',
        content: data.text,
        audioUrl: audioBlobUrl,
        mode: currentMode,
        timestamp: new Date()
      }]);

      // Auto-play audio if input was voice
      if (currentMode === 'voice' && audioBlobUrl) {
        setTimeout(() => playAudio(audioBlobUrl), 300);
      }

    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => [...prev, {
        type: 'error',
        content: `Error: ${error.message}. Please check your connection and try again.`,
        mode: currentMode,
        timestamp: new Date()
      }]);
    } finally {
      setIsLoading(false);
      setInputMode(null);
    }
  };

  // Convert base64 to Blob
  const base64ToBlob = (base64, mimeType) => {
    const byteCharacters = atob(base64);
    const byteNumbers = new Array(byteCharacters.length);
    
    for (let i = 0; i < byteCharacters.length; i++) {
      byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    
    const byteArray = new Uint8Array(byteNumbers);
    return new Blob([byteArray], { type: mimeType });
  };

  // Handle text submit
  const handleTextSubmit = (e) => {
    e.preventDefault();
    if (!inputText.trim() || isLoading) return;
    setInputMode('text');
    sendMessage(inputText);
  };

  // Play audio
  const playAudio = (audioUrl) => {
    if (audioRef.current) {
      audioRef.current.src = audioUrl;
      audioRef.current.play().catch(error => {
        console.error('Error playing audio:', error);
      });
    }
  };

  // Clear chat
  const clearChat = () => {
    if (window.confirm('Are you sure you want to clear the chat?')) {
      setMessages([]);
    }
  };

  // Format timestamp
  const formatTime = (date) => {
    return date.toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      {/* Header */}
      <div className="bg-white shadow-lg px-6 py-4 border-b border-gray-200">
        <div className="flex items-center justify-between max-w-6xl mx-auto">
          <div>
            <h1 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
              🎙️ Voice & Text Assistant
            </h1>
            <p className="text-sm text-gray-600">Speak or type - your choice!</p>
          </div>
          <div className="flex items-center gap-4">
            {/* Language Selector */}
            <div className="flex items-center gap-2 bg-gray-100 rounded-lg px-3 py-2">
              <label className="text-sm font-medium text-gray-700">Language:</label>
              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                className="bg-white border border-gray-300 rounded px-2 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
              >
                <option value="en">English</option>
                <option value="ne">नेपाली (Nepali)</option>
              </select>
            </div>
            
            {messages.length > 0 && (
              <button
                onClick={clearChat}
                className="flex items-center gap-2 px-4 py-2 text-sm text-red-600 hover:bg-red-50 rounded-lg transition-colors"
              >
                <X className="w-4 h-4" />
                Clear
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto px-4 py-6">
        <div className="max-w-4xl mx-auto space-y-4">
          {messages.length === 0 && (
            <div className="text-center text-gray-500 mt-20">
              <div className="text-6xl mb-4">💬</div>
              <p className="text-xl font-medium mb-2">Welcome! How can I help you?</p>
              <p className="text-sm text-gray-400">
                Click the microphone to speak or type your message below
              </p>
            </div>
          )}
          
          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'} animate-fadeIn`}
            >
              <div
                className={`max-w-2xl rounded-2xl px-5 py-3 shadow-md transition-all hover:shadow-lg ${
                  message.type === 'user'
                    ? 'bg-gradient-to-r from-indigo-600 to-indigo-700 text-white'
                    : message.type === 'error'
                    ? 'bg-red-50 text-red-800 border border-red-200'
                    : 'bg-white text-gray-800 border border-gray-100'
                }`}
              >
                <p className="text-base leading-relaxed whitespace-pre-wrap">
                  {message.content}
                </p>
                
                <div className="flex items-center justify-between mt-2 pt-2 border-t border-opacity-20 border-current">
                  <span className="text-xs opacity-70">
                    {message.mode === 'voice' ? '🎤 Voice' : '⌨️ Text'} • {formatTime(message.timestamp)}
                  </span>
                  
                  {message.type === 'assistant' && message.audioUrl && (
                    <button
                      onClick={() => playAudio(message.audioUrl)}
                      className={`p-1.5 rounded-full transition-colors ${
                        message.type === 'user' 
                          ? 'hover:bg-white hover:bg-opacity-20' 
                          : 'hover:bg-gray-100'
                      }`}
                      title="Play audio"
                    >
                      <Volume2 className="w-4 h-4" />
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))}
          
          {isLoading && (
            <div className="flex justify-start animate-fadeIn">
              <div className="bg-white rounded-2xl px-5 py-3 shadow-md border border-gray-100">
                <div className="flex items-center gap-2">
                  <Loader2 className="w-5 h-5 animate-spin text-indigo-600" />
                  <span className="text-sm text-gray-600">Thinking...</span>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input Area */}
      <div className="bg-white border-t border-gray-200 px-4 py-4 shadow-lg">
        <div className="max-w-4xl mx-auto">
          {/* Interim transcript display */}
          {interimTranscript && (
            <div className="mb-3 px-4 py-2 bg-blue-50 text-blue-700 rounded-lg text-sm animate-pulse">
              Listening: "{interimTranscript}"
            </div>
          )}
          
          <form onSubmit={handleTextSubmit}>
            <div className="flex items-end gap-3">
              {/* Voice Button */}
              <button
                type="button"
                onClick={isRecording ? stopRecording : startRecording}
                className={`flex-shrink-0 p-4 rounded-full transition-all shadow-lg transform hover:scale-105 ${
                  isRecording
                    ? 'bg-red-500 hover:bg-red-600 animate-pulse'
                    : 'bg-indigo-600 hover:bg-indigo-700'
                } ${isLoading ? 'opacity-50 cursor-not-allowed' : ''}`}
                disabled={isLoading}
                title={isRecording ? 'Click to stop' : 'Click to speak'}
              >
                {isRecording ? (
                  <MicOff className="w-6 h-6 text-white" />
                ) : (
                  <Mic className="w-6 h-6 text-white" />
                )}
              </button>

              {/* Text Input */}
              <div className="flex-1 relative">
                <textarea
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' && !e.shiftKey) {
                      e.preventDefault();
                      handleTextSubmit(e);
                    }
                  }}
                  placeholder="Type your message or click the mic to speak..."
                  className="w-full px-4 py-3 border-2 border-gray-300 rounded-2xl focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none transition-all"
                  rows="1"
                  disabled={isLoading || isRecording}
                  style={{ minHeight: '52px', maxHeight: '120px' }}
                />
              </div>

              {/* Send Button */}
              <button
                type="submit"
                disabled={!inputText.trim() || isLoading || isRecording}
                className={`flex-shrink-0 p-4 rounded-full transition-all shadow-lg transform hover:scale-105 ${
                  inputText.trim() && !isLoading && !isRecording
                    ? 'bg-indigo-600 hover:bg-indigo-700'
                    : 'bg-gray-300 cursor-not-allowed'
                }`}
                title="Send message"
              >
                <Send className="w-6 h-6 text-white" />
              </button>
            </div>
            
            {isRecording && (
              <p className="text-sm text-red-500 mt-3 text-center font-medium animate-pulse">
                🔴 Recording... Click the microphone to stop
              </p>
            )}
          </form>
        </div>
      </div>

      {/* Hidden audio element */}
      <audio ref={audioRef} className="hidden" />

      {/* Add CSS for animations */}
      <style>{`
        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateY(10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        .animate-fadeIn {
          animation: fadeIn 0.3s ease-out;
        }
      `}</style>
    </div>
  );
};

export default VoiceTextChat;