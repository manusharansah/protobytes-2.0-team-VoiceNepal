# Team Information

**Team Name:** VoiceNepal

**Team Members:**

- Aman Kumar Ray - [@amann45](https://github.com/amann45)
- Aayam Tiwari - [@aayam123](https://github.com/aayam123)
- Dilasha Adhikari - [@dilasha68](https://github.com/dilasha68)
- Manu Sharan Kumar - [@manusharansah](https://github.com/manusharansah)

---

# Project Details

**Project Title:** SajiloSewa Platform

**Category:** E-Governance

**Problem Statement:**
Citizens in Nepal frequently face difficulties understanding documentation requirements, eligibility criteria, and procedural steps for essential government services such as citizenship, passports, and PAN registration. Information is often fragmented or written in complex bureaucratic language, leading to application rejections and multiple visits to government offices.

**Solution Overview:**

SajiloSewa Platform is a voice-enabled e-governance assistant providing instant guidance on passport services in Nepali and English. Citizens receive clear instructions on applications, renewals, documentation, fees, and rejection reasons through voice or text with audio responses for accessibility. The platform offers dual-tier service: public users get 24/7 guidance while administrators manage content via document uploads, voice transcriptions, and a feedback system with ratings and analytics. This continuous improvement loop reduces application errors, office visits, and processing delays, ensuring consistent service delivery independent of government systems.

---

## Technical Stack

**Frontend:** React, JavaScript, Tailwind CSS, Lucide React, Vite

**Backend:** Django, Python 3.9+, Django REST Framework

**Database:** SQLite (for current development)

**AI & NLP:**
- OpenAI API (GPT-4o-mini for chat completions)
- OpenAI Whisper API (voice transcription)
- Vector Store (OpenAI File Storage)

**Text-to-Speech:** gTTS (Google Text-to-Speech)

**Speech-to-Text:** Web Speech API (client-side browser)

**Other Technologies:** 
- python-dotenv (environment management)
- JSON (data storage for feedback)
- Base64 encoding (audio transmission)
- CORS (Cross-Origin Resource Sharing)

---

## Installation & Setup

Follow these steps to get the project running locally.

### Step 1: Clone the Repository

```bash
git clone https://github.com/manusharansah/protobytes-2.0-team-VoiceNepal.git
cd protobytes-2.0-team-VoiceNepal
```

### Step 2: Backend Setup

```bash
# Create and activate a virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Upgrade pip
python -m pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt

# Navigate to Django backend directory
cd backend/voicechat

# Run the Django development server
python manage.py runserver
```

The backend server will be available at `http://127.0.0.1:8000/`

### Step 3: Frontend Setup

Open a new terminal and navigate to the project directory:

```bash
# Navigate to frontend directory
cd my-chat-frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend will be available at `http://localhost:5173/`

---

## Environment Variables

### Backend (.env)

Create a `.env` file in `backend/voicechat/` directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Frontend (.env)

Create a `.env` file in `my-chat-frontend/` directory:

```env
VITE_API_URL=http://127.0.0.1:8000
```

---

## Usage

1. **Open the application** at `http://localhost:5173/`
2. **Select your language** (English or Nepali)
3. **Ask questions** about passport services using voice or text
4. **Receive responses** with both text and audio output

---

## Features

- 🎤 Voice input with speech recognition
- 🔊 Text-to-speech audio responses
- 🌐 Bilingual support (English/Nepali)
- 💬 Real-time chat interface
- 🔐 Admin panel for content management
- 📤 Document upload capability for admin for regular updates
- 💡 Feedback system

---

## Project Structure

```
protobytes-2.0-team-VoiceNepal/
├── backend/
│   └── voicechat/          # Django backend
│       ├── manage.py
│       ├── .env            # Environment variables
│       └── ...
├── my-chat-frontend/        # React frontend
│   ├── src/
│   ├── package.json
│   └── ...
├── requirements.txt
└── README.md
```

---


**Made with ❤️ by Team VoiceNepal**

