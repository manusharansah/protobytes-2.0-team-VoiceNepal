import React, { useState, useRef, useEffect } from "react";
import { 
  Mic, Send, Volume2, Loader2, Trash2, 
  Shield, Upload, FileText, LogOut, User,
  X, Check, AlertCircle, Info, Bot, UserCircle, Square
} from "lucide-react";

// Custom Logo Component
const SajiloSewaLogo = ({ size = 32 }) => (
  <svg width={size} height={size} viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="logoGradient" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" style={{ stopColor: '#3b82f6', stopOpacity: 1 }} />
        <stop offset="100%" style={{ stopColor: '#6366f1', stopOpacity: 1 }} />
      </linearGradient>
    </defs>
    {/* Government building icon */}
    <rect x="20" y="60" width="60" height="30" fill="url(#logoGradient)" rx="2"/>
    <rect x="25" y="40" width="10" height="20" fill="url(#logoGradient)"/>
    <rect x="45" y="40" width="10" height="20" fill="url(#logoGradient)"/>
    <rect x="65" y="40" width="10" height="20" fill="url(#logoGradient)"/>
    <polygon points="50,15 15,45 85,45" fill="url(#logoGradient)"/>
    <circle cx="50" cy="30" r="8" fill="#fff"/>
    <rect x="42" y="70" width="16" height="20" fill="#fff" opacity="0.3"/>
  </svg>
);

const VoiceTextChat = () => {
  const [inputText, setInputText] = useState("");
  const [messages, setMessages] = useState([]);
  const [isRecording, setIsRecording] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [interimTranscript, setInterimTranscript] = useState("");
  const [language, setLanguage] = useState("en");
  const [notification, setNotification] = useState(null);
  
  // Admin state
  const [isAdmin, setIsAdmin] = useState(false);
  const [adminKey, setAdminKey] = useState(localStorage.getItem('admin_key') || "");
  const [showAdminPanel, setShowAdminPanel] = useState(false);
  const [adminTab, setAdminTab] = useState("query");
  const [feedbackMode, setFeedbackMode] = useState(false);
  const [selectedMessage, setSelectedMessage] = useState(null);

  const recognitionRef = useRef(null);
  const messagesEndRef = useRef(null);
  const audioRef = useRef(null);
  const textareaRef = useRef(null);

  // Show notification helper
  const showNotification = (message, type = 'info') => {
    setNotification({ message, type });
    setTimeout(() => setNotification(null), 4000);
  };

  // Scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Auto resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height =
        Math.min(textareaRef.current.scrollHeight, 160) + "px";
    }
  }, [inputText]);

  // Check admin status on mount
  useEffect(() => {
    if (adminKey) {
      checkAdminStatus(adminKey);
    }
  }, []);

  // Speech Recognition
  useEffect(() => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
      recognitionRef.current = null;
    }

    if (!("webkitSpeechRecognition" in window || "SpeechRecognition" in window)) {
      console.warn("Speech recognition not supported");
      return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognitionRef.current = new SpeechRecognition();
    recognitionRef.current.continuous = false;
    recognitionRef.current.interimResults = true;
    recognitionRef.current.lang = language === "ne" ? "ne-NP" : "en-US";

    recognitionRef.current.onstart = () => setIsRecording(true);
    
    recognitionRef.current.onresult = (event) => {
      let interim = "";
      let final = "";

      for (let i = event.resultIndex; i < event.results.length; i++) {
        const transcript = event.results[i][0].transcript;
        if (event.results[i].isFinal) {
          final += transcript;
        } else {
          interim += transcript;
        }
      }

      if (final) {
        setInputText((prev) => (prev + " " + final).trim());
        setInterimTranscript("");
      } else {
        setInterimTranscript(interim);
      }
    };

    recognitionRef.current.onerror = (event) => {
      setIsRecording(false);
      if (event.error === 'not-allowed') {
        showNotification("Microphone access denied", 'error');
      }
    };

    recognitionRef.current.onend = () => {
      setIsRecording(false);
      setInterimTranscript("");
    };

    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
    };
  }, [language]);

  const checkAdminStatus = async (key) => {
    try {
      const response = await fetch("http://localhost:8000/api/check-role/", {
        method: "GET",
        headers: {
          "X-Admin-Key": key,
          "Content-Type": "application/json"
        }
      });
      
      if (!response.ok) return false;
      
      const data = await response.json();
      const adminStatus = data.is_admin === true;
      setIsAdmin(adminStatus);
      return adminStatus;
    } catch (error) {
      return false;
    }
  };

  const saveAdminKey = async (key) => {
    if (!key?.trim()) {
      showNotification("Please enter a valid admin key", 'error');
      return;
    }
    
    const isValidAdmin = await checkAdminStatus(key);
    
    if (isValidAdmin) {
      localStorage.setItem('admin_key', key);
      setAdminKey(key);
      setIsAdmin(true);
      showNotification("Admin access granted", 'success');
    } else {
      showNotification("Invalid admin key", 'error');
    }
  };

  const logout = () => {
    localStorage.removeItem('admin_key');
    setAdminKey("");
    setIsAdmin(false);
    setShowAdminPanel(false);
    showNotification("Logged out successfully", 'success');
  };

  const goHome = () => {
    if (recognitionRef.current && isRecording) {
      recognitionRef.current.stop();
    }
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
    }
    setInputText("");
    setInterimTranscript("");
    setMessages([]);
    setShowAdminPanel(false);
    setFeedbackMode(false);
    setSelectedMessage(null);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const stripMarkdownAsterisks = (text = "") =>
    String(text)
      .replace(/\*\*(.*?)\*\*/g, "$1")
      .replace(/\*(.*?)\*/g, "$1")
      .replace(/\*/g, "")
      .trim();

  const sendMessage = async (text) => {
    if (!text.trim()) return;

    const userMessage = { type: "user", content: text };
    setMessages((prev) => [...prev, userMessage]);
    setInputText("");
    setIsLoading(true);

    try {
      const headers = { "Content-Type": "application/json" };
      if (isAdmin && adminKey) {
        headers["X-Admin-Key"] = adminKey;
      }

      const response = await fetch("http://localhost:8000/api/chat/", {
        method: "POST",
        headers,
        body: JSON.stringify({ text, language }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `HTTP ${response.status}`);
      }

      const data = await response.json();
      if (data.error) throw new Error(data.error);

      const audioBlob = new Blob(
        [Uint8Array.from(atob(data.audio_base64), (c) => c.charCodeAt(0))],
        { type: "audio/mp3" }
      );

      const audioUrl = URL.createObjectURL(audioBlob);

      const assistantMessage = { 
        type: "assistant", 
        content: stripMarkdownAsterisks(data.text), 
        audioUrl,
        role: data.role,
        timestamp: data.timestamp || null,
        response_id: data.response_id || null,
        question: text
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      showNotification(error.message, 'error');
      setMessages((prev) => [
        ...prev,
        {
          type: "assistant",
          content: `I apologize, but I encountered an error. Please try again.`,
          isError: true
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const playAudio = (url) => {
    if (audioRef.current) {
      audioRef.current.src = url;
      audioRef.current.play().catch(err => console.error("Audio error:", err));
    }
  };

  const stopAudio = () => {
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage(inputText);
    }
  };

  const toggleRecording = () => {
    if (!recognitionRef.current) {
      showNotification("Speech recognition not available", 'error');
      return;
    }

    if (isRecording) {
      recognitionRef.current.stop();
    } else {
      try {
        recognitionRef.current.start();
      } catch (error) {
        showNotification("Could not start voice recognition", 'error');
      }
    }
  };

  const submitFeedback = async (message, feedbackData) => {
    if (!isAdmin || !adminKey) {
      showNotification("Admin access required", 'error');
      return;
    }

    try {
      const response = await fetch("http://localhost:8000/api/admin/feedback/", {
        method: "POST",
        headers: { 
          "Content-Type": "application/json",
          "X-Admin-Key": adminKey
        },
        body: JSON.stringify({
          question: message.question || "N/A",
          response: message.content,
          feedback_type: feedbackData.type,
          feedback_text: feedbackData.text,
          rating: feedbackData.rating
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error);
      }

      const result = await response.json();
      
      if (result.status === "success") {
        showNotification("Feedback submitted successfully", 'success');
        setFeedbackMode(false);
        setSelectedMessage(null);
      }
    } catch (error) {
      showNotification("Failed to submit feedback", 'error');
    }
  };

  const uploadDocument = async (file) => {
    if (!isAdmin || !adminKey) {
      showNotification("Admin access required", 'error');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch("http://localhost:8000/api/admin/upload-document/", {
        method: "POST",
        headers: { "X-Admin-Key": adminKey },
        body: formData
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error);
      }

      const result = await response.json();
      
      if (result.status === "success") {
        showNotification(`Document "${file.name}" uploaded successfully`, 'success');
      }
    } catch (error) {
      showNotification(`Upload failed: ${error.message}`, 'error');
    }
  };

  const uploadText = async (filename, content) => {
    if (!isAdmin || !adminKey) {
      showNotification("Admin access required", 'error');
      return;
    }

    try {
      const response = await fetch("http://localhost:8000/api/admin/upload-text/", {
        method: "POST",
        headers: { 
          "Content-Type": "application/json",
          "X-Admin-Key": adminKey
        },
        body: JSON.stringify({ filename, content })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error);
      }

      const result = await response.json();
      
      if (result.status === "success") {
        showNotification(`Text "${filename}" uploaded successfully`, 'success');
      }
    } catch (error) {
      showNotification(`Upload failed: ${error.message}`, 'error');
    }
  };

  return (
    <div className="h-screen flex flex-col bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      {/* Overlay for Admin Panel */}
      {isAdmin && showAdminPanel && (
        <div 
          className="fixed inset-0 bg-black/20 backdrop-blur-sm z-40 animate-fade-in"
          onClick={() => setShowAdminPanel(false)}
        />
      )}

      {/* Notification Toast */}
      {notification && (
        <div className="fixed top-4 right-4 z-50 animate-slide-in-right">
          <div className={`flex items-center gap-3 px-4 py-3 rounded-xl shadow-2xl backdrop-blur-md ${
            notification.type === 'success' ? 'bg-emerald-500/90 text-white' :
            notification.type === 'error' ? 'bg-red-500/90 text-white' :
            'bg-blue-500/90 text-white'
          }`}>
            {notification.type === 'success' && <Check size={18} />}
            {notification.type === 'error' && <AlertCircle size={18} />}
            {notification.type === 'info' && <Info size={18} />}
            <span className="font-medium text-sm">{notification.message}</span>
          </div>
        </div>
      )}

      {/* HEADER */}
      <header className="bg-white/90 backdrop-blur-xl border-b border-gray-200/50 shadow-sm sticky top-0 z-40">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <div className="flex justify-between items-center">
            {/* Logo and Title */}
            <button
              type="button"
              onClick={goHome}
              className="flex items-center gap-4 text-left group"
              title="Go to home"
            >
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-br from-blue-400 to-indigo-500 rounded-2xl blur opacity-30 animate-pulse-slow"></div>
                <div className="relative bg-white p-2 rounded-2xl shadow-lg group-hover:shadow-xl transition-all">
                  <SajiloSewaLogo size={40} />
                </div>
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 bg-clip-text text-transparent">
                  SajiloSewa - Passport Services
                </h1>
                <p className="text-xs text-gray-600 font-medium flex items-center gap-2">
                  <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
                  Passport Application Assistant
                  {isAdmin && <span className="ml-2 px-2 py-0.5 bg-amber-100 text-amber-700 text-xs rounded-full font-semibold">Admin</span>}
                </p>
              </div>
            </button>

            {/* Controls */}
            <div className="flex items-center gap-3">
              {/* Language Selector */}
              <div className="relative group">
                <select
                  value={language}
                  onChange={(e) => {
                    setLanguage(e.target.value);
                    if (isRecording && recognitionRef.current) {
                      recognitionRef.current.stop();
                    }
                  }}
                  className="appearance-none bg-white border-2 border-gray-200 hover:border-blue-400 rounded-xl px-4 py-2.5 pr-10 text-sm font-medium focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all cursor-pointer shadow-sm hover:shadow-md"
                >
                  <option value="en">🇬🇧 English</option>
                  <option value="ne">🇳🇵 नेपाली</option>
                </select>
                <div className="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none">
                  <svg className="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </div>
              </div>

              {/* Admin Panel Button */}
              {isAdmin && (
                <button
                  onClick={() => setShowAdminPanel(!showAdminPanel)}
                  className="relative p-2.5 rounded-xl bg-gradient-to-br from-amber-400 to-orange-500 text-white hover:shadow-lg hover:scale-105 transition-all group"
                  title="Admin Panel"
                >
                  <Shield size={20} />
                  <span className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full animate-ping"></span>
                  <span className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full"></span>
                </button>
              )}

              {/* Clear Chat */}
              {messages.length > 0 && (
                <button
                  onClick={() => {
                    if (window.confirm("Clear all messages?")) {
                      setMessages([]);
                      showNotification("Chat cleared", 'info');
                    }
                  }}
                  className="p-2.5 rounded-xl text-gray-600 hover:text-red-600 hover:bg-red-50 transition-all"
                  title="Clear chat"
                >
                  <Trash2 size={20} />
                </button>
              )}

              {/* Admin Login/Logout */}
              {!isAdmin ? (
                <button
                  onClick={() => {
                    const key = prompt("Enter admin key:");
                    if (key) saveAdminKey(key);
                  }}
                  className="p-2.5 rounded-xl text-gray-600 hover:text-blue-600 hover:bg-blue-50 transition-all"
                  title="Admin Login"
                >
                  <User size={20} />
                </button>
              ) : (
                <button
                  onClick={logout}
                  className="p-2.5 rounded-xl text-gray-600 hover:text-red-600 hover:bg-red-50 transition-all"
                  title="Logout"
                >
                  <LogOut size={20} />
                </button>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* ADMIN PANEL - RIGHT SIDEBAR */}
      {isAdmin && showAdminPanel && (
        <div className="fixed right-0 top-0 h-full w-96 bg-gradient-to-br from-amber-50 to-orange-50 border-l border-amber-200 shadow-2xl z-50 overflow-y-auto animate-slide-in-right">
          <div className="p-6">
            {/* Admin Panel Header */}
            <div className="flex justify-between items-center mb-6">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-gradient-to-br from-amber-400 to-orange-500 rounded-xl text-white">
                  <Shield size={24} />
                </div>
                <div>
                  <h3 className="text-xl font-bold text-gray-800">Admin Panel</h3>
                  <p className="text-xs text-gray-600">Manage content & feedback</p>
                </div>
              </div>
              <button
                onClick={() => setShowAdminPanel(false)}
                className="p-2 rounded-xl hover:bg-white/50 transition-all"
                title="Close panel"
              >
                <X size={20} />
              </button>
            </div>

            {/* Tab Navigation */}
            <div className="flex flex-col gap-2 mb-6">
              {['query', 'upload', 'feedback'].map((tab) => (
                <button
                  key={tab}
                  onClick={() => {
                    setAdminTab(tab);
                    if (tab === 'feedback') setFeedbackMode(!feedbackMode);
                  }}
                  className={`w-full px-5 py-3.5 rounded-xl text-sm font-semibold transition-all flex items-center gap-3 ${
                    adminTab === tab
                      ? "bg-gradient-to-r from-amber-500 to-orange-500 text-white shadow-lg"
                      : "bg-white text-gray-700 hover:bg-amber-100"
                  }`}
                >
                  {tab === 'query' && (
                    <>
                      <span className="text-xl">💭</span>
                      <span>Query Mode</span>
                    </>
                  )}
                  {tab === 'upload' && (
                    <>
                      <span className="text-xl">📤</span>
                      <span>Upload Documents</span>
                    </>
                  )}
                  {tab === 'feedback' && (
                    <>
                      <span className="text-xl">💡</span>
                      <span>Feedback System</span>
                    </>
                  )}
                </button>
              ))}
            </div>

            {/* Tab Content */}
            <div className="space-y-4">
              {adminTab === "query" && (
                <div className="bg-white rounded-2xl p-5 shadow-sm border border-amber-200">
                  <h4 className="font-bold text-gray-800 mb-3 flex items-center gap-2">
                    <span className="text-xl">💭</span>
                    Query Mode Active
                  </h4>
                  <p className="text-sm text-gray-700 mb-4">
                    You're in admin query mode. Your questions will be prioritized and marked with an admin badge.
                  </p>
                  <div className="bg-amber-50 border-2 border-amber-200 rounded-xl p-4">
                    <p className="text-xs text-amber-800 font-semibold mb-2">✨ Admin Benefits:</p>
                    <ul className="text-xs text-amber-700 space-y-1">
                      <li>• Priority response handling</li>
                      <li>• Access to detailed analytics</li>
                      <li>• Special admin badge on messages</li>
                    </ul>
                  </div>
                </div>
              )}

              {adminTab === "upload" && (
                <AdminUploadPanel 
                  onUploadDocument={uploadDocument}
                  onUploadText={uploadText}
                />
              )}

              {adminTab === "feedback" && (
                <div className="bg-white rounded-2xl p-5 shadow-sm border border-amber-200">
                  <h4 className="font-bold text-gray-800 mb-3 flex items-center gap-2">
                    <span className="text-xl">💡</span>
                    Feedback System
                  </h4>
                  <div className="bg-blue-50 border-2 border-blue-200 rounded-xl p-4 mb-4">
                    <p className="text-sm text-gray-700 mb-2">
                      <span className="font-bold">Status:</span>{' '}
                      {feedbackMode ? 
                        <span className="text-green-600 font-semibold">🟢 Active</span> : 
                        <span className="text-gray-500">⚪ Inactive</span>
                      }
                    </p>
                    {feedbackMode && (
                      <p className="text-xs text-blue-700">
                        Click any assistant message in the chat to provide feedback.
                      </p>
                    )}
                  </div>
                  <button
                    onClick={() => setFeedbackMode(!feedbackMode)}
                    className={`w-full px-5 py-3.5 rounded-xl text-sm font-semibold transition-all ${
                      feedbackMode
                        ? "bg-gradient-to-r from-red-500 to-red-600 text-white hover:shadow-lg"
                        : "bg-gradient-to-r from-amber-500 to-orange-500 text-white hover:shadow-lg"
                    }`}
                  >
                    {feedbackMode ? "🔴 Disable Feedback Mode" : "🟢 Enable Feedback Mode"}
                  </button>
                  
                  {feedbackMode && (
                    <div className="mt-4 bg-green-50 border-2 border-green-200 rounded-xl p-4 animate-fade-in">
                      <p className="text-xs text-green-800 font-semibold mb-2">📝 How to use:</p>
                      <ol className="text-xs text-green-700 space-y-1 list-decimal list-inside">
                        <li>Browse through chat messages</li>
                        <li>Click on any assistant response</li>
                        <li>Fill in the feedback form</li>
                        <li>Submit for analysis</li>
                      </ol>
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* Quick Stats (Optional Enhancement) */}
            <div className="mt-6 bg-white rounded-2xl p-5 shadow-sm border border-amber-200">
              <h4 className="font-bold text-gray-800 mb-3 flex items-center gap-2">
                <span className="text-xl">📊</span>
                Session Stats
              </h4>
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl p-3 border border-blue-200">
                  <p className="text-xs text-blue-600 font-semibold mb-1">Messages</p>
                  <p className="text-2xl font-bold text-blue-700">{messages.length}</p>
                </div>
                <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-xl p-3 border border-green-200">
                  <p className="text-xs text-green-600 font-semibold mb-1">Admin</p>
                  <p className="text-2xl font-bold text-green-700">
                    {messages.filter(m => m.role === 'admin').length}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* CHAT AREA */}
      <main className="flex-1 overflow-y-auto px-6 py-8">
        <div className="max-w-4xl mx-auto space-y-6">
          {messages.length === 0 && (
            <div className="text-center mt-20 animate-fade-in">
              <div className="relative inline-block mb-8">
                <div className="absolute inset-0 bg-gradient-to-br from-blue-400 to-indigo-500 rounded-3xl blur-2xl opacity-20 animate-pulse-slow"></div>
                <div className="relative bg-white p-6 rounded-3xl shadow-2xl">
                  <SajiloSewaLogo size={64} />
                </div>
              </div>
              
              <h2 className="text-3xl font-bold text-gray-800 mb-3 bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                Namaste! How can we assist you with your passport?
              </h2>
              <p className="text-gray-600 mb-2 max-w-xl mx-auto text-lg">
                Your trusted guide for passport applications,<br/>renewals, and all passport-related services
              </p>
              <p className="text-sm text-gray-500 mb-10 flex items-center justify-center gap-2">
                <Mic size={16} className="text-blue-500" />
                Voice input: {language === "ne" ? "नेपाली" : "English"}
              </p>

              {/* Quick Actions - Passport Only */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 max-w-3xl mx-auto mb-8">
                {[
                  { icon: "🛂", title: "New Passport", desc: "First-time application" },
                  { icon: "🔄", title: "Renewal", desc: "Renew your passport" },
                  { icon: "📋", title: "Requirements", desc: "Documents needed" }
                ].map((item, i) => (
                  <button
                    key={i}
                    onClick={() => sendMessage(`How to apply for ${item.title.toLowerCase()}?`)}
                    className="group bg-white rounded-2xl p-6 border-2 border-gray-200 hover:border-blue-400 hover:shadow-xl transition-all text-left"
                  >
                    <div className="text-3xl mb-3">{item.icon}</div>
                    <h3 className="font-bold text-gray-800 mb-1 group-hover:text-blue-600 transition-colors">{item.title}</h3>
                    <p className="text-sm text-gray-500">{item.desc}</p>
                  </button>
                ))}
              </div>

              {/* Quick Suggestions - Passport Only */}
              <div className="flex flex-wrap gap-3 justify-center max-w-2xl mx-auto">
                {[
                  "What documents do I need for a new passport?",
                  "How long does passport renewal take?",
                  "What are the passport fees?",
                  "Can I track my passport application?"
                ].map((suggestion, i) => (
                  <button
                    key={i}
                    onClick={() => sendMessage(suggestion)}
                    className="px-5 py-2.5 bg-white border-2 border-gray-200 rounded-full text-sm text-gray-700 font-medium hover:border-blue-400 hover:bg-gradient-to-r hover:from-blue-50 hover:to-indigo-50 hover:text-blue-700 transition-all shadow-sm hover:shadow-md"
                  >
                    {suggestion}
                  </button>
                ))}
              </div>
            </div>
          )}

          {messages.map((msg, i) => (
            <div
              key={i}
              className={`flex ${msg.type === "user" ? "justify-end" : "justify-start"} animate-slide-up`}
            >
              <div className={`flex gap-3 max-w-2xl ${msg.type === "user" ? "flex-row-reverse" : "flex-row"}`}>
                {/* Avatar */}
                <div className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center ${
                  msg.type === "user" 
                    ? "bg-gradient-to-br from-blue-500 to-indigo-600" 
                    : msg.isError
                    ? "bg-gradient-to-br from-red-400 to-red-600"
                    : "bg-gradient-to-br from-emerald-400 to-teal-600"
                }`}>
                  {msg.type === "user" ? (
                    <UserCircle size={24} className="text-white" />
                  ) : (
                    <Bot size={24} className="text-white" />
                  )}
                </div>

                {/* Message Content */}
                <div
                  onClick={() => {
                    if (feedbackMode && msg.type === "assistant" && !msg.isError) {
                      setSelectedMessage(msg);
                    }
                  }}
                  className={`px-6 py-4 rounded-2xl shadow-md transition-all ${
                    msg.type === "user"
                      ? "bg-gradient-to-br from-blue-500 to-indigo-600 text-white"
                      : msg.isError
                      ? "bg-red-50 border-2 border-red-200 text-red-700"
                      : "bg-white border-2 border-gray-100"
                  } ${
                    feedbackMode && msg.type === "assistant" && !msg.isError
                      ? "cursor-pointer hover:ring-4 hover:ring-amber-200"
                      : ""
                  }`}
                >
                  <p className="text-sm leading-relaxed whitespace-pre-wrap">
                    {msg.content}
                  </p>

                  {msg.role === "admin" && (
                    <div className="mt-3 inline-flex items-center gap-1.5 px-3 py-1 bg-amber-100 text-amber-700 text-xs rounded-full font-semibold">
                      <Shield size={12} />
                      Admin Query
                    </div>
                  )}

                  {msg.audioUrl && (
                    <div className="mt-4 flex items-center gap-2">
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          playAudio(msg.audioUrl);
                        }}
                        className="flex items-center gap-2 text-xs font-semibold text-blue-600 hover:text-blue-700 bg-blue-50 px-4 py-2 rounded-full hover:bg-blue-100 transition-all shadow-sm hover:shadow-md"
                      >
                        <Volume2 size={16} />
                        Play Audio
                      </button>
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          stopAudio();
                        }}
                        className="flex items-center gap-2 text-xs font-semibold text-red-600 hover:text-red-700 bg-red-50 px-4 py-2 rounded-full hover:bg-red-100 transition-all shadow-sm hover:shadow-md"
                      >
                        <Square size={14} />
                        Stop
                      </button>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}

          {isLoading && (
            <div className="flex justify-start animate-slide-up">
              <div className="flex gap-3">
                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-emerald-400 to-teal-600 flex items-center justify-center">
                  <Bot size={24} className="text-white" />
                </div>
                <div className="bg-white border-2 border-gray-100 px-6 py-4 rounded-2xl flex items-center gap-3 text-sm text-gray-600 shadow-md">
                  <Loader2 className="animate-spin text-blue-600" size={18} />
                  <span className="font-medium">Preparing your guidance...</span>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </main>

      {/* INPUT AREA */}
      <div className="bg-white/90 backdrop-blur-xl border-t border-gray-200/50 px-6 py-6 shadow-2xl">
        <div className="max-w-4xl mx-auto">
          <div className="relative">
            <div className="flex items-end gap-3 bg-white rounded-2xl border-2 border-gray-200 shadow-lg p-3 focus-within:border-blue-500 focus-within:ring-4 focus-within:ring-blue-100 transition-all">
              {/* Voice Button */}
              <button
                onClick={toggleRecording}
                disabled={!recognitionRef.current}
                className={`relative p-4 rounded-xl transition-all flex-shrink-0 ${
                  isRecording
                    ? "bg-gradient-to-br from-red-500 to-red-600 text-white shadow-lg shadow-red-200 scale-110"
                    : "bg-gradient-to-br from-gray-100 to-gray-200 text-gray-700 hover:from-blue-500 hover:to-indigo-600 hover:text-white hover:shadow-md disabled:opacity-40 disabled:cursor-not-allowed"
                }`}
                title={isRecording ? "Stop recording" : `Voice input (${language === "ne" ? "Nepali" : "English"})`}
              >
                <Mic size={22} className={isRecording ? "animate-pulse" : ""} />
                {isRecording && (
                  <span className="absolute -top-1 -right-1 flex h-3 w-3">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
                    <span className="relative inline-flex rounded-full h-3 w-3 bg-red-500"></span>
                  </span>
                )}
              </button>

              {/* Text Input */}
              <textarea
                ref={textareaRef}
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder={language === "ne" 
                  ? "तपाईंको पासपोर्ट सम्बन्धी प्रश्न यहाँ लेख्नुहोस्..." 
                  : "Ask about passport applications, renewals, requirements..."}
                rows={1}
                className="flex-1 resize-none bg-transparent px-3 py-3 text-sm focus:outline-none placeholder-gray-400 text-gray-800"
              />

              {/* Send Button */}
              <button
                onClick={() => sendMessage(inputText)}
                disabled={!inputText.trim() || isLoading}
                className="p-4 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 text-white hover:shadow-lg hover:scale-105 disabled:opacity-40 disabled:cursor-not-allowed disabled:hover:scale-100 transition-all flex-shrink-0"
                title="Send message"
              >
                <Send size={22} />
              </button>
            </div>

            {/* Interim Transcript */}
            {interimTranscript && (
              <div className="mt-3 flex items-center gap-3 text-sm text-gray-600 bg-blue-50 px-4 py-2 rounded-lg">
                <div className="flex gap-1">
                  <span className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></span>
                  <span className="w-2 h-2 bg-red-500 rounded-full animate-pulse" style={{ animationDelay: '0.2s' }}></span>
                  <span className="w-2 h-2 bg-red-500 rounded-full animate-pulse" style={{ animationDelay: '0.4s' }}></span>
                </div>
                <span className="font-medium italic">
                  Listening ({language === "ne" ? "नेपाली" : "English"}): {interimTranscript}
                </span>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* FEEDBACK MODAL */}
      {selectedMessage && (
        <FeedbackModal
          message={selectedMessage}
          onClose={() => setSelectedMessage(null)}
          onSubmit={(feedbackData) => submitFeedback(selectedMessage, feedbackData)}
        />
      )}

      <audio ref={audioRef} hidden />

      <style jsx>{`
        @keyframes slide-up {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        @keyframes fade-in {
          from {
            opacity: 0;
          }
          to {
            opacity: 1;
          }
        }

        @keyframes slide-in-right {
          from {
            opacity: 0;
            transform: translateX(100px);
          }
          to {
            opacity: 1;
            transform: translateX(0);
          }
        }

        @keyframes pulse-slow {
          0%, 100% {
            opacity: 0.3;
          }
          50% {
            opacity: 0.6;
          }
        }

        .animate-slide-up {
          animation: slide-up 0.4s ease-out;
        }

        .animate-fade-in {
          animation: fade-in 0.6s ease-out;
        }

        .animate-slide-in-right {
          animation: slide-in-right 0.3s ease-out;
        }

        .animate-pulse-slow {
          animation: pulse-slow 3s ease-in-out infinite;
        }
      `}</style>
    </div>
  );
};

// Admin Upload Panel Component
const AdminUploadPanel = ({ onUploadDocument, onUploadText }) => {
  const [uploadType, setUploadType] = useState("document");
  const [textFilename, setTextFilename] = useState("");
  const [textContent, setTextContent] = useState("");
  const fileInputRef = useRef(null);

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      onUploadDocument(file);
      e.target.value = null;
    }
  };

  const handleTextUpload = () => {
    if (!textFilename.trim() || !textContent.trim()) {
      alert("Please enter both filename and content");
      return;
    }
    
    onUploadText(textFilename.trim(), textContent);
    setTextFilename("");
    setTextContent("");
  };

  return (
    <div className="bg-white rounded-2xl p-6 shadow-sm border border-amber-200">
      <div className="flex gap-2 mb-6">
        <button
          onClick={() => setUploadType("document")}
          className={`flex-1 px-4 py-3 rounded-xl text-sm font-semibold transition-all ${
            uploadType === "document"
              ? "bg-gradient-to-r from-blue-500 to-indigo-600 text-white shadow-md"
              : "bg-gray-100 text-gray-700 hover:bg-gray-200"
          }`}
        >
          📄 Document
        </button>
        <button
          onClick={() => setUploadType("text")}
          className={`flex-1 px-4 py-3 rounded-xl text-sm font-semibold transition-all ${
            uploadType === "text"
              ? "bg-gradient-to-r from-blue-500 to-indigo-600 text-white shadow-md"
              : "bg-gray-100 text-gray-700 hover:bg-gray-200"
          }`}
        >
          📝 Text
        </button>
      </div>

      {uploadType === "document" && (
        <div>
          <input
            ref={fileInputRef}
            type="file"
            onChange={handleFileUpload}
            accept=".pdf,.txt,.doc,.docx"
            className="hidden"
          />
          <button
            onClick={() => fileInputRef.current?.click()}
            className="w-full bg-gradient-to-r from-blue-500 to-indigo-600 text-white py-4 px-6 rounded-xl hover:shadow-lg transition-all flex items-center justify-center gap-3 font-semibold"
          >
            <Upload size={20} />
            Choose Document
          </button>
          <p className="text-xs text-gray-500 mt-3 text-center font-medium">
            Supported: PDF, TXT, DOC, DOCX (Max 10MB)
          </p>
        </div>
      )}

      {uploadType === "text" && (
        <div className="space-y-4">
          <input
            type="text"
            value={textFilename}
            onChange={(e) => setTextFilename(e.target.value)}
            placeholder="Filename (e.g., passport_policy_update)"
            className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          <textarea
            value={textContent}
            onChange={(e) => setTextContent(e.target.value)}
            placeholder="Enter passport-related content..."
            rows={6}
            className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
          />
          <button
            onClick={handleTextUpload}
            className="w-full bg-gradient-to-r from-blue-500 to-indigo-600 text-white py-4 px-6 rounded-xl hover:shadow-lg transition-all flex items-center justify-center gap-3 font-semibold"
          >
            <FileText size={20} />
            Upload Text
          </button>
        </div>
      )}
    </div>
  );
};

// Feedback Modal Component
const FeedbackModal = ({ message, onClose, onSubmit }) => {
  const [feedbackType, setFeedbackType] = useState("improvement");
  const [feedbackText, setFeedbackText] = useState("");
  const [rating, setRating] = useState(3);

  const handleSubmit = () => {
    if (!feedbackText.trim()) {
      alert("Please enter feedback text");
      return;
    }

    onSubmit({
      type: feedbackType,
      text: feedbackText,
      rating: rating
    });
  };

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4 animate-fade-in">
      <div className="bg-white rounded-3xl shadow-2xl max-w-lg w-full p-8 animate-slide-up">
        <div className="flex justify-between items-center mb-6">
          <h3 className="text-2xl font-bold text-gray-800">
            Submit Feedback
          </h3>
          <button
            onClick={onClose}
            className="p-2 rounded-xl hover:bg-gray-100 transition-all"
          >
            <X size={24} />
          </button>
        </div>

        <div className="mb-6">
          <label className="block text-sm font-semibold text-gray-700 mb-3">
            Response:
          </label>
          <div className="bg-gray-50 p-4 rounded-xl text-sm text-gray-700 max-h-32 overflow-y-auto border-2 border-gray-200">
            {message.content}
          </div>
        </div>

        <div className="mb-6">
          <label className="block text-sm font-semibold text-gray-700 mb-3">
            Feedback Type:
          </label>
          <select
            value={feedbackType}
            onChange={(e) => setFeedbackType(e.target.value)}
            className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="correction">🔧 Correction</option>
            <option value="improvement">💡 Improvement</option>
            <option value="positive">👍 Positive</option>
            <option value="negative">👎 Negative</option>
          </select>
        </div>

        <div className="mb-6">
          <label className="block text-sm font-semibold text-gray-700 mb-3">
            Rating: {rating}/5
          </label>
          <input
            type="range"
            min="1"
            max="5"
            value={rating}
            onChange={(e) => setRating(Number(e.target.value))}
            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
          />
          <div className="flex justify-between text-xs text-gray-500 mt-2">
            <span>Poor</span>
            <span>Excellent</span>
          </div>
        </div>

        <div className="mb-6">
          <label className="block text-sm font-semibold text-gray-700 mb-3">
            Detailed Feedback:
          </label>
          <textarea
            value={feedbackText}
            onChange={(e) => setFeedbackText(e.target.value)}
            placeholder="Share your thoughts..."
            rows={4}
            className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
          />
        </div>

        <div className="flex gap-3">
          <button
            onClick={onClose}
            className="flex-1 bg-gray-100 text-gray-700 py-3 px-6 rounded-xl hover:bg-gray-200 transition-all font-semibold"
          >
            Cancel
          </button>
          <button
            onClick={handleSubmit}
            className="flex-1 bg-gradient-to-r from-blue-500 to-indigo-600 text-white py-3 px-6 rounded-xl hover:shadow-lg transition-all font-semibold"
          >
            Submit Feedback
          </button>
        </div>
      </div>
    </div>
  );
};

export default VoiceTextChat;
