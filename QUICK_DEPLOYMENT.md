# Quick Deployment Fix for Vercel Connection Issue

## Problem
Your Vercel deployment is trying to connect to `http://localhost:5000` instead of your production backend.

## Solution

### Step 1: Deploy Backend to Render

1. **Go to Render Dashboard**: https://dashboard.render.com/
2. **Create New Blueprint**: Click "New +" → "Blueprint"
3. **Connect Repository**: Connect your GitHub repository
4. **Render will auto-detect** the `render.yaml` file
5. **Set Environment Variables**:
   - `GOOGLE_CLIENT_ID`: Your Google OAuth client ID
   - `GOOGLE_CLIENT_SECRET`: Your Google OAuth client secret
   - `NOTION_TOKEN`: Your Notion integration token (optional)
   - `NOTION_PARENT_PAGE_ID`: Your Notion page ID (optional)
   - `FRONTEND_URL`: Your Vercel frontend URL (set after Vercel deployment)
6. **Click "Apply"** to deploy

### Step 2: Update Vercel Environment Variables

1. **Go to Vercel Dashboard**: https://vercel.com/dashboard
2. **Select your project**
3. **Go to Settings** → **Environment Variables**
4. **Add these variables**:
   - `REACT_APP_API_BASE_URL`: `https://your-backend-service-name.onrender.com`
   - `REACT_APP_WHISPER_API_URL`: `https://your-whisper-service-name.onrender.com`
5. **Redeploy** your Vercel project

### Step 3: Update Backend CORS

After getting your Vercel URL, update the `FRONTEND_URL` environment variable in your Render backend service.

## Current Status

✅ **Fixed**: Added fallback URLs in code (will work temporarily)
✅ **Ready**: Updated `render.yaml` for deployment
✅ **Ready**: Fixed `vercel.json` configuration

## Next Steps

1. Deploy to Render using the steps above
2. Update Vercel environment variables
3. Test your application

## Troubleshooting

- **Backend not responding**: Check Render service logs
- **CORS errors**: Ensure `FRONTEND_URL` is set correctly in Render
- **Environment variables not working**: Redeploy Vercel after setting variables 