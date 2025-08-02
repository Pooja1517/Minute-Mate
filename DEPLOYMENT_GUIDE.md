# Deployment Guide for Minute Mate

This guide will help you deploy your Minute Mate application to production.

## Prerequisites

- GitHub account
- Vercel account (free)
- Render account (free)
- Google Cloud Console access (for OAuth)
- Notion integration (optional)

## Step 1: Prepare Your Repository

1. **Commit all changes to GitHub:**
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Verify your repository structure:**
   ```
   minute-mate/
   ├── client/          # React frontend
   ├── server/          # Node.js backend
   ├── whisper_api.py   # Python Whisper API
   ├── vercel.json      # Vercel config
   ├── render.yaml      # Render config
   └── requirements.txt # Python dependencies
   ```

## Step 2: Deploy Backend Services to Render

### 2.1 Deploy Node.js Backend

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `minute-mate-backend`
   - **Environment**: `Node`
   - **Build Command**: `cd server && npm install`
   - **Start Command**: `cd server && node index.js`
   - **Plan**: Free

5. **Set Environment Variables:**
   - `NODE_ENV`: `production`
   - `GOOGLE_CLIENT_ID`: Your Google OAuth client ID
   - `GOOGLE_CLIENT_SECRET`: Your Google OAuth client secret
   - `NOTION_TOKEN`: Your Notion integration token
   - `NOTION_PARENT_PAGE_ID`: Your Notion page ID
   - `FRONTEND_URL`: Your Vercel frontend URL (set after Step 3)

6. Click "Create Web Service"

### 2.2 Deploy Python Whisper API

1. In Render Dashboard, click "New +" → "Web Service"
2. Connect the same GitHub repository
3. Configure the service:
   - **Name**: `minute-mate-whisper`
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python whisper_api.py`
   - **Plan**: Free

4. **Set Environment Variables:**
   - `NOTION_TOKEN`: Your Notion integration token
   - `NOTION_DATABASE_ID`: Your Notion database ID

5. Click "Create Web Service"

## Step 3: Deploy Frontend to Vercel

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "New Project"
3. Import your GitHub repository
4. Configure the project:
   - **Framework Preset**: Other
   - **Root Directory**: `client`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`

5. **Set Environment Variables:**
   - `REACT_APP_API_BASE_URL`: `https://your-backend-url.onrender.com`
   - `REACT_APP_WHISPER_API_URL`: `https://your-whisper-api-url.onrender.com`

6. Click "Deploy"

## Step 4: Update URLs and Redeploy

1. **Update Backend Environment Variables:**
   - Go to your Render backend service
   - Update `FRONTEND_URL` with your Vercel URL
   - Redeploy the service

2. **Update Frontend Environment Variables:**
   - Go to your Vercel project settings
   - Update the API URLs with your actual Render URLs
   - Redeploy the frontend

## Step 5: Configure Google OAuth

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Update your OAuth 2.0 credentials:
   - Add `https://your-backend-url.onrender.com/auth/google/callback` to authorized redirect URIs
   - Add your Vercel frontend URL to authorized JavaScript origins

## Step 6: Test Your Deployment

1. **Test Frontend**: Visit your Vercel URL
2. **Test Backend Health**: `https://your-backend-url.onrender.com/health`
3. **Test Whisper API**: `https://your-whisper-api-url.onrender.com/health`
4. **Test Audio Upload**: Try uploading a small audio file
5. **Test Export Features**: Test Google Docs and Notion exports

## Troubleshooting

### Common Issues:

1. **CORS Errors**: Ensure all URLs are properly configured
2. **Environment Variables**: Double-check all environment variables are set
3. **Build Failures**: Check build logs for missing dependencies
4. **Whisper Model Loading**: The first request may take longer as models load

### Performance Notes:

- **Free Tier Limitations**: Render free tier has cold starts and limited resources
- **Whisper Model**: Uses "small" model for faster processing
- **File Size**: Limited to 10MB for audio files
- **Memory**: Optimized for large files with cleanup and delays

## Monitoring

- **Render Logs**: Monitor service logs in Render dashboard
- **Vercel Analytics**: Enable analytics in Vercel dashboard
- **Health Checks**: Use `/health` endpoints to monitor services

## Scaling Considerations

For production use with high traffic:
- Upgrade to paid Render plans for better performance
- Consider using larger Whisper models for better accuracy
- Implement caching for transcriptions
- Add rate limiting and authentication
- Use CDN for static assets

## Support

If you encounter issues:
1. Check the service logs in Render/Vercel dashboards
2. Verify all environment variables are set correctly
3. Test locally first to isolate issues
4. Check the health endpoints for service status 