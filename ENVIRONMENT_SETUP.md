# Environment Setup Guide

## The Problem You're Experiencing

When you stop the backend servers, the frontend can't connect to them because it's trying to reach `localhost:5000` and `localhost:5001`. This is expected behavior, but we can make the error messages more helpful.

## Solution: Environment Variables

### For Local Development

Create a file called `.env.local` in the `client` folder:

```bash
# client/.env.local
REACT_APP_API_BASE_URL=http://localhost:5000
REACT_APP_WHISPER_API_URL=http://localhost:5001
```

### For Production Deployment

When you deploy to Vercel, set these environment variables:

```bash
REACT_APP_API_BASE_URL=https://your-backend-url.onrender.com
REACT_APP_WHISPER_API_URL=https://your-whisper-api-url.onrender.com
```

## How to Test

1. **Start both servers locally:**
   ```bash
   # Terminal 1 - Backend
   cd server && npm start
   
   # Terminal 2 - Whisper API
   python whisper_api.py
   
   # Terminal 3 - Frontend
   cd client && npm start
   ```

2. **Test with servers running:** Should work normally

3. **Test with servers stopped:** Should show helpful error message

## Current Status

✅ **Fixed Issues:**
- AudioRecorder component now uses environment variables
- TranscriptDashboard component now uses environment variables
- Better error handling for connection failures
- Clear error messages when backend is not available

## Error Messages You'll See

When the backend is stopped, you'll now see:
- "Cannot connect to backend server. Please make sure the backend is running on http://localhost:5000"
- Instead of generic "Transcription failed" messages

## Next Steps

1. **For local development:** Create the `.env.local` file in the client folder
2. **For deployment:** Set environment variables in Vercel dashboard
3. **Test:** Try stopping/starting your backend servers to see the improved error messages

## Troubleshooting

If you still see connection issues:

1. **Check if servers are running:**
   - Backend: `http://localhost:5000/health`
   - Whisper API: `http://localhost:5001/health`

2. **Check browser console:** Look for the actual error messages

3. **Verify environment variables:** Make sure they're set correctly

4. **Restart frontend:** After changing environment variables, restart the React app 