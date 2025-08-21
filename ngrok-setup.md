# ngrok Local Development Setup

## 🚀 Quick Setup for Local Development

### Step 1: Install ngrok
```bash
# Install ngrok globally
npm install -g ngrok

# Or download from https://ngrok.com/download
```

### Step 2: Start Your Local Whisper Service
```bash
# Navigate to your project directory
cd minute-mate

# Install dependencies
pip install -r requirements-render-minimal.txt

# Start the Whisper service locally
python whisper_render_fix.py
```

### Step 3: Expose Local Service with ngrok
```bash
# In a new terminal, expose your local service
ngrok http 5001

# You'll get a public HTTPS URL like:
# https://abc123.ngrok.io
```

### Step 4: Update Frontend Configuration
```javascript
// Update your frontend to use the ngrok URL
const WHISPER_URL = "https://abc123.ngrok.io"; // Your ngrok URL

// Test the connection
fetch(`${WHISPER_URL}/health`)
  .then(response => response.json())
  .then(data => console.log('Service status:', data));
```

## 🔧 Environment Variables for Local Development

Create a `.env` file in your project root:
```env
NOTION_TOKEN=your_notion_token_here
NOTION_DATABASE_ID=your_database_id_here
FLASK_ENV=development
```

## 📱 Testing the Local Setup

1. **Health Check**: `https://your-ngrok-url.ngrok.io/health`
2. **Transcription**: Upload audio file via your frontend
3. **Notion Export**: Test saving to Notion
4. **Google Docs Export**: Test formatting for Google Docs

## ⚠️ Important Notes

- **ngrok URLs change** every time you restart ngrok (free plan)
- **Not for production** - only for development/testing
- **Keep your local machine running** while testing
- **Update frontend URL** when ngrok URL changes

## 🎯 Benefits of Local Development

✅ **Fast iteration** - no deployment delays
✅ **Full control** - easy to debug and modify
✅ **No resource limits** - use your local machine's power
✅ **Immediate testing** - see changes instantly
✅ **Cost-free** - no cloud hosting costs

## 🚀 Next Steps

1. **Set up ngrok** and test locally
2. **Verify all features work** (transcription, Notion, Google Docs)
3. **Choose best deployment option** based on testing results
4. **Deploy to production** when ready

This gives you a working solution while you decide on the best production deployment option! 