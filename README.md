# Minute Mate - AI Meeting Assistant

An AI-powered meeting assistant that transcribes audio and generates meeting summaries and action items.

## 🚀 Quick Start

### Prerequisites
- Node.js installed
- Python 3.8+ installed
- Git repository cloned

### Step 1: Start Backend Services

#### Start Node.js Backend (Port 5000)
```bash
cd server
npm install
node index.js
```

#### Start Python Whisper API (Port 5001)
```bash
# In a new terminal
python -m pip install -r requirements.txt
python whisper_api.py
```

### Step 2: Start Frontend (Port 3000)
```bash
cd client
npm install
npm start
```

### Step 3: Test Local Setup
1. Open http://localhost:3000
2. Record or upload an audio file
3. Should work with local backend services

## 📁 Project Structure

```
minute-mate/
├── client/          # React frontend (Port 3000)
├── server/          # Node.js backend (Port 5000)
├── whisper_api.py   # Python Whisper API (Port 5001)
├── requirements.txt # Python dependencies
└── render.yaml      # Render deployment config (optional)
```

## 🔧 Features

- 🎤 **Audio Recording**: Record meetings directly in the browser
- 📁 **File Upload**: Upload existing audio files
- 🤖 **AI Transcription**: Powered by OpenAI Whisper
- 📝 **Smart Summaries**: AI-generated meeting summaries
- ✅ **Action Items**: Extract tasks and action items
- 📤 **Export Options**: Google Docs and Notion integration

## 🧪 Testing

Your local setup should work with:
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:5000
- **Whisper API**: http://localhost:5001

## 🎯 Result

Your app works seamlessly in local development:
- **Simple Setup**: No complex environment variables
- **Hardcoded URLs**: Direct localhost connections
- **Clean Codebase**: Focused on local development
