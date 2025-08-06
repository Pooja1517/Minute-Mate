# Environment Variable Setup Guide

This guide shows you exactly how to configure environment variables for both local development and Vercel production.

## 🏠 Local Development Setup

### Step 1: Create Local Environment File

Create a file called `.env.local` in the `client/` directory:

```bash
# Navigate to client directory
cd client

# Create .env.local file
echo "REACT_APP_API_BASE_URL=http://localhost:5000" > .env.local
echo "REACT_APP_WHISPER_API_URL=http://localhost:5001" >> .env.local
```

**File content (`client/.env.local`):**
```env
# Local Development Environment Variables
REACT_APP_API_BASE_URL=http://localhost:5000
REACT_APP_WHISPER_API_URL=http://localhost:5001
```

### Step 2: Verify Local Setup

1. Start your local services:
   ```bash
   # Terminal 1: Backend
   cd server && npm install && node index.js
   
   # Terminal 2: Whisper API
   python -m pip install -r requirements.txt && python whisper_api.py
   
   # Terminal 3: Frontend
   cd client && npm install && npm start
   ```

2. Open browser console and check:
   ```javascript
   // Should show:
   // Hostname: localhost
   // Environment Variable: http://localhost:5000
   // Final API URL: http://localhost:5000
   ```

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

### Step 2: Configure Vercel Environment Variables

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Select your project
3. Go to **Settings** → **Environment Variables**
4. Add these variables:

   **Variable 1:**
   - **Name**: `REACT_APP_API_BASE_URL`
   - **Value**: `https://your-backend-service-name.onrender.com`
   - **Environment**: Production, Preview, Development

   **Variable 2:**
   - **Name**: `REACT_APP_WHISPER_API_URL`
   - **Value**: `https://your-whisper-service-name.onrender.com`
   - **Environment**: Production, Preview, Development

5. Click **Save**
6. **Redeploy** your project

### Step 3: Verify Production Setup

1. Visit your Vercel URL
2. Open browser console and check:
   ```javascript
   // Should show:
   // Hostname: your-vercel-domain.vercel.app
   // Environment Variable: https://your-backend-service-name.onrender.com
   // Final API URL: https://your-backend-service-name.onrender.com
   ```

## 🔧 How It Works

### Environment Detection Logic

The app uses this priority system:

1. **Environment Variable** (highest priority)
   - If `REACT_APP_API_BASE_URL` is set, use it
   - This is what Vercel will use in production

2. **Local Development Detection**
   - If hostname is `localhost` or `127.0.0.1`, use localhost URLs
   - This ensures local development works without environment variables

3. **Production Fallback** (lowest priority)
   - If neither above, use Render URLs as fallback
   - This provides a safety net

### Code Implementation

```javascript
// In AudioRecorder.js
const getApiBaseUrl = () => {
  if (process.env.REACT_APP_API_BASE_URL) {
    return process.env.REACT_APP_API_BASE_URL;  // Vercel production
  }
  
  if (window.location.hostname === 'localhost') {
    return "http://localhost:5000";  // Local development
  }
  
  return "https://minute-mate-backend.onrender.com";  // Fallback
};
```

## 🧪 Testing

### Test Local Development
```bash
# Start all services locally
cd server && npm install && node index.js
python -m pip install -r requirements.txt && python whisper_api.py
cd client && npm install && npm start

# Should connect to localhost:5000 and localhost:5001
```

### Test Vercel Production
1. Deploy to Render and Vercel
2. Set environment variables in Vercel dashboard
3. Visit your Vercel URL
4. Should connect to Render backend services

## ✅ Success Checklist

### Local Development
- [ ] `.env.local` file created in `client/` directory
- [ ] Local backend running on port 5000
- [ ] Local Whisper API running on port 5001
- [ ] Frontend connects to localhost URLs
- [ ] Audio transcription works locally

### Vercel Production
- [ ] Backend deployed on Render
- [ ] Whisper API deployed on Render
- [ ] Environment variables set in Vercel dashboard
- [ ] Frontend connects to Render URLs
- [ ] Audio transcription works on Vercel

## 🐛 Troubleshooting

### "Cannot connect to backend server"
- **Local**: Check if backend services are running
- **Vercel**: Verify environment variables are set correctly

### Environment variables not working
- **Vercel**: Redeploy after setting environment variables
- **Local**: Restart React development server after creating `.env.local`

### CORS errors
- Ensure `FRONTEND_URL` is set in Render backend
- Check that URLs match exactly (no trailing slashes)

## 🎯 Result

After following this guide:
- **Local development**: Uses `http://localhost:5000` and `http://localhost:5001`
- **Vercel production**: Uses your Render backend URLs
- **Automatic detection**: No manual switching required
- **Both environments work perfectly** ✅ 