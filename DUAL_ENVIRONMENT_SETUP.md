# Dual Environment Setup - Local + Vercel

This guide ensures your Minute Mate app works perfectly both locally and on Vercel.

## 🏠 Local Development Setup

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

## 🌐 Vercel Production Setup

### Step 1: Deploy Backend to Render
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "Blueprint"
3. Connect your GitHub repository
4. Set environment variables:
   - `GOOGLE_CLIENT_ID`: Your Google OAuth client ID
   - `GOOGLE_CLIENT_SECRET`: Your Google OAuth client secret
   - `NOTION_TOKEN`: Your Notion integration token (optional)
   - `NOTION_PARENT_PAGE_ID`: Your Notion page ID (optional)
   - `FRONTEND_URL`: Your Vercel frontend URL
5. Click "Apply"

### Step 2: Deploy Frontend to Vercel
1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Import your GitHub repository
3. Set environment variables:
   - `REACT_APP_API_BASE_URL`: `https://your-backend-service-name.onrender.com`
   - `REACT_APP_WHISPER_API_URL`: `https://your-whisper-service-name.onrender.com`
4. Deploy

## 🔧 Environment Detection Logic

The app automatically detects the environment:

### Local Development
- **Backend**: `http://localhost:5000`
- **Whisper API**: `http://localhost:5001`

### Production (Vercel)
- **Backend**: `https://minute-mate-backend.onrender.com`
- **Whisper API**: `https://minute-mate-whisper.onrender.com`

## 🚀 Quick Start Scripts

### Start Everything Locally
```bash
# Terminal 1: Backend
cd server && npm install && node index.js

# Terminal 2: Whisper API
python -m pip install -r requirements.txt && python whisper_api.py

# Terminal 3: Frontend
cd client && npm install && npm start
```

### Deploy to Production
```bash
# Commit changes
git add .
git commit -m "Update for production"
git push origin main

# Deploy to Render (follow dashboard steps)
# Deploy to Vercel (follow dashboard steps)
```

## 🧪 Testing Both Environments

### Test Local
1. Start all local services
2. Visit http://localhost:3000
3. Upload audio file
4. Verify transcription works

### Test Vercel
1. Deploy to Render and Vercel
2. Visit your Vercel URL
3. Upload audio file
4. Verify transcription works

## 🔍 Debugging

### Check Environment Detection
Open browser console and check:
```javascript
console.log('Hostname:', window.location.hostname);
console.log('API URL:', process.env.REACT_APP_API_BASE_URL);
```

### Common Issues
- **Local not working**: Check if backend services are running on correct ports
- **Vercel not working**: Check environment variables in Vercel dashboard
- **CORS errors**: Ensure FRONTEND_URL is set in Render backend

## 📁 File Structure
```
minute-mate/
├── client/          # React frontend (Port 3000)
├── server/          # Node.js backend (Port 5000)
├── whisper_api.py   # Python Whisper API (Port 5001)
├── render.yaml      # Render deployment config
└── vercel.json      # Vercel deployment config
```

## ✅ Success Checklist

### Local Development
- [ ] Backend running on http://localhost:5000
- [ ] Whisper API running on http://localhost:5001
- [ ] Frontend running on http://localhost:3000
- [ ] Audio upload and transcription working

### Vercel Production
- [ ] Backend deployed on Render
- [ ] Whisper API deployed on Render
- [ ] Frontend deployed on Vercel
- [ ] Environment variables set correctly
- [ ] Audio upload and transcription working

## 🎯 Result
Your app will work seamlessly in both environments:
- **Local**: For development and testing
- **Vercel**: For production and sharing 