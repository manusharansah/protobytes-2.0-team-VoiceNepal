# Team Information

**Team Name:** VoiceNepal

**Team Members:**

- Aman Patel - [@amann45](https://github.com/amann45)
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
SajiloSewa Platform is a voice-enabled e-governance information service designed to act as a shared guidance layer across multiple government applications. It provides clear documentation requirements, step-by-step procedural guidance, office-level instructions, and common rejection reasons through voice and text interaction in Nepali and English. The platform leverages a Retrieval-Augmented Generation (RAG) architecture to deliver accurate, up-to-date, and context-aware guidance by retrieving relevant information from a curated knowledge base, ensuring consistent, accessible, and scalable service support without direct dependency on government web APIs.


## Installation & Setup

Follow these steps to get the project running locally.

```bash
# 1. Clone the repository
git clone https://github.com/manusharansah/protobytes-2.0-team-VoiceNepal.git
cd protobytes-2.0-team-VoiceNepal

# 2. Create and activate a virtual environment
python -m venv venv
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scripts\activate


# 3. Install project dependencies
python.exe -m pip install --upgrade pip
pip install -r requirements.txt



# 5. Run the Django development server
cd backend/voicechat
echo "OPENAI_API_KEY=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
" > .env

python manage.py runserver

# 6. Open http://127.0.0.1:8000/ in your browser