# Production Setup Guide

## ✅ **Your Frontend Now Works with Deployed Backends!**

I've updated your frontend to use production URLs by default. Now when you stop your local backend servers, your frontend will automatically connect to the deployed services on Render.

## 🔧 **What I Changed:**

### **Updated URLs:**
- **Backend API**: `https://minute-mate-backend.onrender.com`
- **Whisper API**: `https://minute-mate-whisper.onrender.com`

### **Files Updated:**
- `client/src/App.js` - Whisper API URL
- `client/src/components/AudioRecorder.js` - Backend API URL  
- `client/src/components/TranscriptDashboard.js` - Backend API URL

## 🚀 **How to Deploy Your Backend Services:**

### **Step 1: Deploy to Render**

1. **Go to [Render Dashboard](https://dashboard.render.com/)**
2. **Create two web services:**

#### **Backend Service (Node.js):**
- **Name**: `minute-mate-backend`
- **Environment**: `Node`
- **Build Command**: `cd server && npm install`
- **Start Command**: `cd server && node index.js`
- **Plan**: Free

#### **Whisper Service (Python):**
- **Name**: `minute-mate-whisper`
- **Environment**: `Python`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python whisper_api.py`
- **Plan**: Free

### **Step 2: Set Environment Variables in Render**

#### **For Backend Service:**
```
NODE_ENV=production
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
NOTION_TOKEN=your_notion_token
NOTION_PARENT_PAGE_ID=your_notion_page_id
FRONTEND_URL=https://your-vercel-frontend-url.vercel.app
```

#### **For Whisper Service:**
```
NOTION_TOKEN=your_notion_token
NOTION_DATABASE_ID=your_notion_database_id
```

### **Step 3: Deploy Frontend to Vercel**

1. **Go to [Vercel Dashboard](https://vercel.com/dashboard)**
2. **Import your GitHub repository**
3. **Configure:**
   - **Framework Preset**: Other
   - **Root Directory**: `client`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`

4. **Set Environment Variables:**
   ```
   REACT_APP_API_BASE_URL=https://minute-mate-backend.onrender.com
   REACT_APP_WHISPER_API_URL=https://minute-mate-whisper.onrender.com
   ```

## 🧪 **Testing:**

### **With Local Backend Running:**
- Frontend will use localhost URLs (if you set environment variables)
- Everything works as before

### **With Local Backend Stopped:**
- Frontend will use production URLs automatically
- Connects to deployed services on Render
- No more connection errors!

## 🔄 **Environment Variable Priority:**

1. **Environment Variables** (highest priority)
2. **Production URLs** (default fallback)
3. **Localhost URLs** (only if explicitly set)

## 📝 **For Local Development:**

If you want to use localhost during development, create a `.env.local` file in the `client` folder:

```bash
# client/.env.local
REACT_APP_API_BASE_URL=http://localhost:5000
REACT_APP_WHISPER_API_URL=http://localhost:5001
```

## 🎯 **Result:**

Now your frontend will work seamlessly whether your local backend is running or not! It will automatically connect to the deployed services when local servers are stopped.

## ⚠️ **Important Notes:**

- **First deployment**: Render services may take a few minutes to start up
- **Cold starts**: Free tier services may have delays on first request
- **CORS**: Make sure your Render services allow requests from your Vercel domain
- **Environment variables**: Double-check all environment variables are set correctly

Your application is now production-ready! 🎉 