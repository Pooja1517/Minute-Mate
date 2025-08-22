# 🚀 Quick ngrok Testing Setup

## **Immediate Testing While Render Deploys**

This guide lets you test your app immediately using ngrok, bypassing deployment delays.

## 📋 **Prerequisites**

1. **Install ngrok**:
   ```bash
   # Option 1: npm (if you have Node.js)
   npm install -g ngrok
   
   # Option 2: Download from https://ngrok.com/
   # Extract and add to PATH
   ```

2. **Sign up for free ngrok account** at https://ngrok.com/
3. **Get your authtoken** from ngrok dashboard

## 🔧 **Setup Steps**

### **Step 1: Authenticate ngrok**
```bash
ngrok config add-authtoken YOUR_AUTH_TOKEN_HERE
```

### **Step 2: Start Your Local Services**

**Terminal 1 - Whisper API:**
```bash
cd server
python ../whisper_render_fix.py
# Should start on http://127.0.0.1:5001
```

**Terminal 2 - Node.js Backend:**
```bash
cd server
npm start
# Should start on http://localhost:5000
```

**Terminal 3 - React Frontend:**
```bash
cd client
npm start
# Should start on http://localhost:3000
```

### **Step 3: Expose Backend with ngrok**

**Terminal 4 - ngrok:**
```bash
ngrok http 5000
# This exposes your Node.js backend
```

You'll see output like:
```
Forwarding    https://abc123.ngrok.io -> http://localhost:5000
```

### **Step 4: Update Frontend Configuration**

In `client/src/components/AudioRecorder.js`, update the API URL:
```javascript
// Change this line:
const API_BASE_URL = "http://localhost:5000";

// To your ngrok URL:
const API_BASE_URL = "https://abc123.ngrok.io";
```

In `client/src/App.js`, update the Whisper API URL:
```javascript
// Change this line:
const WHISPER_API_URL = "http://localhost:5001";

// To your ngrok URL (but port 5001):
const WHISPER_API_URL = "https://abc123.ngrok.io:5001";
```

**Wait!** Since ngrok only exposes one port, you need to expose the Whisper service too:

**Terminal 5 - ngrok for Whisper:**
```bash
ngrok http 5001
# This exposes your Whisper API
```

Now update the Whisper URL in `App.js` to use the second ngrok URL.

## 🧪 **Test Your Setup**

1. **Visit your frontend**: http://localhost:3000
2. **Record or upload audio** (keep files < 3MB)
3. **Test transcription** - should work through ngrok
4. **Test Google Docs export** - should work through ngrok
5. **Test Notion export** - should work through ngrok

## ⚠️ **Important Notes**

- **ngrok URLs change** every time you restart ngrok (free plan)
- **File size limits** still apply (3MB max for testing)
- **Performance** may be slower than local testing
- **HTTPS** is provided by ngrok automatically

## 🔄 **Alternative: Single ngrok Tunnel**

If you want to use just one ngrok tunnel, you can:

1. **Expose only the Node.js backend** (port 5000)
2. **Update the Whisper service** to also run on port 5000
3. **Use different routes** for backend vs Whisper API

## 🚨 **Troubleshooting**

### **ngrok not working?**
- Check if authtoken is set correctly
- Verify ports 5000 and 5001 are not blocked
- Check firewall settings

### **Services not connecting?**
- Verify all services are running
- Check console for error messages
- Ensure ngrok URLs are correct

### **CORS issues?**
- Your CORS is already configured for this setup
- If issues persist, check browser console

## 🎯 **Next Steps**

1. **Test everything works** with ngrok
2. **Deploy to Render** using the optimized configuration
3. **Switch from ngrok** to Render URLs
4. **Enjoy your working app!**

---

**💡 Pro Tip**: Keep ngrok running in a separate terminal while you test, so you don't lose your URLs!
