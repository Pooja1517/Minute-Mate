# MinuteMate Setup Guide

## 🔧 Complete Setup for Local & Production

### Step 1: Google Cloud Console Setup

1. **Go to:** https://console.cloud.google.com/
2. **Select your project:** `minutemate-467409`
3. **Enable Google Docs API:**
   - Go to: https://console.cloud.google.com/apis/library
   - Search for "Google Docs API"
   - Click "Enable"

4. **Configure OAuth Credentials:**
   - Go to: https://console.cloud.google.com/apis/credentials
   - Edit your OAuth 2.0 Client ID
   - Add these redirect URIs:
     ```
     http://localhost:5000/auth/google/callback
     https://minute-mate.onrender.com/auth/google/callback
     ```
   - Save changes

### Step 2: Local Environment Setup

1. **Create `.env` file in `server/` directory:**
   ```env
   # Google OAuth2 Credentials
   GOOGLE_CLIENT_ID=your_google_client_id_here
   GOOGLE_CLIENT_SECRET=your_google_client_secret_here
   
   # Frontend URL for local development
   FRONTEND_URL=http://localhost:3000
   
   # Environment
   NODE_ENV=development
   ```

2. **Get your Google credentials:**
   - Go to: https://console.cloud.google.com/apis/credentials
   - Copy your OAuth 2.0 Client ID and Client Secret
   - Replace `your_google_client_id_here` and `your_google_client_secret_here`

### Step 3: Production Environment Setup

1. **Render Environment Variables:**
   - Go to your Render dashboard
   - Select your backend service
   - Go to "Environment" tab
   - Add these variables:
     ```
     GOOGLE_CLIENT_ID=your_google_client_id_here
     GOOGLE_CLIENT_SECRET=your_google_client_secret_here
     FRONTEND_URL=https://minute-mate-omega.vercel.app
     NODE_ENV=production
     ```

### Step 4: Test Both Environments

#### Local Testing:
```bash
# Terminal 1: Start Whisper API
python whisper_api_mock.py

# Terminal 2: Start Backend
cd server
node index.js

# Terminal 3: Start Frontend
cd client
npm start
```

#### Production Testing:
- Go to: https://minute-mate-omega.vercel.app

### Step 5: Verify Google Docs Export

1. **Upload an audio file**
2. **Click "Transcribe"**
3. **Click "Export to Google Docs"**
4. **Sign in with Google**
5. **Grant permissions**
6. **Should get a direct link to the document**

## 🐛 Troubleshooting

### "No refresh token is set"
- Make sure you're using the correct Google credentials
- Check that OAuth flow requests `offline` access
- Verify redirect URIs are exact matches

### "redirect_uri_mismatch"
- Double-check redirect URIs in Google Cloud Console
- Make sure no extra spaces or typos
- Wait 2-3 minutes after saving changes

### "Google Docs API not enabled"
- Go to Google Cloud Console → APIs & Services → Library
- Search for "Google Docs API"
- Click "Enable"

## ✅ Success Indicators

- ✅ Transcription works on both local and live
- ✅ Google Docs export gives direct document link
- ✅ No OAuth errors
- ✅ Works after page refresh

## 📞 Need Help?

- Check the browser console (F12) for error messages
- Verify all environment variables are set
- Test with the live version first: https://minute-mate-omega.vercel.app 