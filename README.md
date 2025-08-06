# Minute Mate - AI Meeting Assistant

An AI-powered meeting assistant that transcribes audio and generates meeting summaries and action items.

## 🚀 Quick Start

### Local Development
```bash
# Start all services locally
powershell -ExecutionPolicy Bypass -File start_local.ps1

# Then run these in separate terminals:
# Terminal 1: Backend
cd server && npm install && node index.js

# Terminal 2: Whisper API  
python -m pip install -r requirements.txt && python whisper_api.py

# Terminal 3: Frontend
cd client && npm install && npm start
```

### Production Deployment
```bash
# Deploy to Render (Backend)
powershell -ExecutionPolicy Bypass -File deploy_to_render.ps1

# Deploy to Vercel (Frontend)
# Follow the guide in QUICK_DEPLOYMENT.md
```

## 🌐 Environment Support

✅ **Local Development**: http://localhost:3000  
✅ **Vercel Production**: Your Vercel URL  
✅ **Automatic Environment Detection**: App detects local vs production

## 📁 Project Structure

```
minute-mate/
├── client/          # React frontend (Port 3000)
├── server/          # Node.js backend (Port 5000)
├── whisper_api.py   # Python Whisper API (Port 5001)
├── render.yaml      # Render deployment config
├── vercel.json      # Vercel deployment config
└── *.ps1           # PowerShell startup scripts
```

## 🔧 Features

- 🎤 **Audio Recording**: Record meetings directly in the browser
- 📁 **File Upload**: Upload existing audio files
- 🤖 **AI Transcription**: Powered by OpenAI Whisper
- 📝 **Smart Summaries**: AI-generated meeting summaries
- ✅ **Action Items**: Extract tasks and action items
- 📤 **Export Options**: Google Docs and Notion integration

## 📚 Documentation

- [DUAL_ENVIRONMENT_SETUP.md](DUAL_ENVIRONMENT_SETUP.md) - Complete setup guide
- [QUICK_DEPLOYMENT.md](QUICK_DEPLOYMENT.md) - Production deployment
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Detailed deployment guide

## 🧪 Testing

```bash
# Test local setup
powershell -ExecutionPolicy Bypass -File test_local_setup.ps1
```

## 🎯 Result

Your app works seamlessly in both environments:
- **Local**: For development and testing
- **Vercel**: For production and sharing
