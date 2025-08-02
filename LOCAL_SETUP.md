# MinuteMate Local Development Setup

This guide will help you set up MinuteMate to run locally on your machine.

## Prerequisites

- Node.js (v16 or higher)
- Python (v3.8 or higher)
- npm or yarn
- pip

## Quick Setup (Windows)

1. **Run the setup script:**
   ```powershell
   .\setup_local_dev.ps1
   ```
   
   Or if you prefer batch:
   ```cmd
   .\setup_local_dev.bat
   ```

2. **Start the services in separate terminals:**

   **Terminal 1 - Whisper API (Python):**
   ```bash
   python whisper_api.py
   ```
   
   **Terminal 2 - Node.js Server:**
   ```bash
   cd server
   node index.js
   ```
   
   **Terminal 3 - React Frontend:**
   ```bash
   cd client
   npm start
   ```

3. **Open your browser:**
   Navigate to `http://localhost:3000`

## Manual Setup

If you prefer to set up manually:

### 1. Install Dependencies

```bash
# Python dependencies
pip install -r requirements.txt

# Node.js dependencies
cd server && npm install
cd ../client && npm install
```

### 2. Create Environment Files

**Create `server/.env`:**
```env
# Server Configuration
NODE_ENV=development
PORT=5000

# Google OAuth Configuration (optional)
GOOGLE_CLIENT_ID=your-google-client-id-here
GOOGLE_CLIENT_SECRET=your-google-client-secret-here
FRONTEND_URL=http://localhost:3000

# Notion Configuration (optional)
NOTION_TOKEN=your-notion-integration-token-here
NOTION_PARENT_PAGE_ID=your-parent-page-id-here

# Whisper API Configuration
WHISPER_API_URL=http://localhost:5001
```

**Create `client/.env`:**
```env
REACT_APP_API_URL=http://localhost:5000
REACT_APP_WHISPER_API_URL=http://localhost:5001
```

### 3. Start Services

Start all three services in separate terminals:

**Whisper API (Port 5001):**
```bash
python whisper_api.py
```

**Node.js Server (Port 5000):**
```bash
cd server
node index.js
```

**React Frontend (Port 3000):**
```bash
cd client
npm start
```

## Service Architecture

- **Frontend (React)**: `http://localhost:3000` - User interface
- **Backend (Node.js)**: `http://localhost:5000` - File uploads, OAuth, exports
- **Whisper API (Python)**: `http://localhost:5001` - Audio transcription and AI processing

## Troubleshooting

### "No transcript received from backend" Error

This usually means:
1. **Whisper API not running** - Make sure `python whisper_api.py` is running
2. **Node.js server not running** - Make sure `node index.js` is running in the server directory
3. **Wrong API URLs** - Check that your `.env` files point to localhost

### Port Already in Use

If you get port conflicts:
- Kill existing processes: `netstat -ano | findstr :5000` then `taskkill /PID <PID>`
- Or change ports in the `.env` files

### Python Dependencies Issues

If you get Python import errors:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Node.js Dependencies Issues

If you get npm errors:
```bash
cd server && npm install
cd ../client && npm install
```

## Testing the Setup

1. **Test Whisper API:**
   ```bash
   curl -X POST http://localhost:5001/transcribe
   ```
   Should return: `{"error":"No audio file uploaded"}`

2. **Test Node.js Server:**
   ```bash
   curl http://localhost:5000/health
   ```
   Should return: `{"status":"healthy","service":"minute-mate-backend"}`

3. **Test Frontend:**
   Open `http://localhost:3000` in your browser

## Optional Features

### Google Docs Export
To enable Google Docs export:
1. Create a Google Cloud Project
2. Enable Google Docs API
3. Create OAuth 2.0 credentials
4. Update `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` in `server/.env`

### Notion Export
To enable Notion export:
1. Create a Notion integration at https://www.notion.so/my-integrations
2. Get your integration token
3. Create a page and share it with your integration
4. Update `NOTION_TOKEN` and `NOTION_PARENT_PAGE_ID` in `server/.env`

## Development Workflow

1. Make changes to your code
2. Services will auto-reload (except for environment variable changes)
3. For environment variable changes, restart the affected service
4. Test your changes in the browser

## Production Deployment

For production deployment, see the main README.md file for instructions on deploying to Render and Vercel. 