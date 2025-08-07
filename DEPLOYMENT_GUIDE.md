# Render Deployment Guide - Whisper API Fixes

## Issues Fixed

### 1. RAM Limitations
- **Problem**: Whisper models require significant memory, especially on Render's free tier
- **Solution**: 
  - Changed from "small" to "base" model (smaller memory footprint)
  - Added fallback to "tiny" model if base fails
  - Reduced file size limit from 10MB to 5MB

### 2. Dependencies (ffmpeg)
- **Problem**: Whisper requires ffmpeg for audio processing, not included by default
- **Solution**:
  - Created `build.sh` script to install ffmpeg and other system dependencies
  - Added `ffmpeg-python` to requirements.txt
  - Created Dockerfile as alternative approach

### 3. Timeouts
- **Problem**: Long transcription processes can timeout on Render free tier
- **Solution**:
  - Optimized transcription settings for memory efficiency
  - Disabled fp16 for better compatibility
  - Added better error handling and logging

### 4. Frontend Build Issues
- **Problem**: React app deployment failing with pip build errors
- **Solution**:
  - Added proper frontend service configuration to render.yaml
  - Updated React dependencies to stable versions
  - Added .npmrc for better npm behavior
  - Used `npm ci` for more reliable builds

### 5. Python __version__ KeyError
- **Problem**: Python packages missing `__version__` attribute causing build failures
- **Solution**:
  - Created multiple requirements files with different version strategies
  - Added setuptools and wheel upgrades in build scripts
  - Created minimal requirements file for essential packages only
  - Added `--no-cache-dir` and `--force-reinstall` flags

## Deployment Options

### Option 1: Standard Build (Recommended)
Use the updated `render.yaml` with all three services:
- Frontend (React static site)
- Backend (Node.js)
- Whisper API (Python with build script)

### Option 2: Stable Build (Alternative)
Use `render-stable.yaml` for more conservative package versions:
```yaml
buildCommand: chmod +x build-stable.sh && ./build-stable.sh
```

### Option 3: Minimal Build (Troubleshooting)
Use `requirements-minimal.txt` and `build-minimal.sh` for essential packages only.

### Option 4: Docker Build (Alternative)
Use `render-docker.yaml` for Docker-based Whisper deployment:
```yaml
env: docker
dockerfilePath: ./Dockerfile
```

## Services Configuration

### Frontend Service
```yaml
- type: web
  name: minute-mate-frontend
  env: static
  plan: free
  buildCommand: cd client && npm ci --only=production && npm run build
  staticPublishPath: ./client/build
```

### Backend Service
```yaml
- type: web
  name: minute-mate-backend
  env: node
  plan: free
  buildCommand: cd server && npm install
  startCommand: cd server && node index.js
```

### Whisper Service
```yaml
- type: web
  name: minute-mate-whisper
  env: python
  plan: free
  buildCommand: chmod +x build.sh && ./build.sh
  startCommand: python whisper_api.py
```

## Key Changes Made

1. **whisper_api.py**:
   - Removed Windows-specific ffmpeg path
   - Changed model from "small" to "base"
   - Added fallback to "tiny" model
   - Reduced file size limit to 5MB
   - Optimized transcription settings

2. **requirements.txt**:
   - Added `ffmpeg-python==0.2.0`
   - Added `notion-client==2.2.1`
   - Added `setuptools>=65.0.0` and `wheel>=0.38.0`

3. **build.sh**:
   - Installs ffmpeg and audio processing libraries
   - Upgrades pip and setuptools
   - Uses `--no-cache-dir` and `--force-reinstall` flags

4. **Dockerfile**:
   - Alternative approach using Docker
   - Ensures all system dependencies are available

5. **client/package.json**:
   - Updated React to stable version 18.2.0
   - Fixed dependency version conflicts
   - Updated testing libraries

6. **client/.npmrc**:
   - Added npm configuration for reliable builds
   - Enabled legacy peer deps

7. **render.yaml**:
   - Added frontend service configuration
   - Proper static site deployment setup

8. **Alternative Files**:
   - `requirements-stable.txt` - Conservative versions
   - `requirements-minimal.txt` - Essential packages only
   - `build-stable.sh` and `build-minimal.sh` - Alternative build scripts
   - `render-stable.yaml` - Alternative deployment config

## Environment Variables Required

### Frontend
- `REACT_APP_BACKEND_URL` - URL of your backend service
- `REACT_APP_WHISPER_URL` - URL of your Whisper service

### Backend
- `NODE_ENV` - Set to "production"
- `GOOGLE_CLIENT_ID` - Google OAuth client ID
- `GOOGLE_CLIENT_SECRET` - Google OAuth client secret
- `NOTION_TOKEN` - Notion integration token
- `NOTION_PARENT_PAGE_ID` - Notion parent page ID
- `FRONTEND_URL` - URL of your frontend service

### Whisper API
- `NOTION_TOKEN` - Notion integration token
- `NOTION_DATABASE_ID` - Notion database ID
- `PYTHONUNBUFFERED` - Set to "1"
- `FLASK_ENV` - Set to "production"

## Testing the Deployment

1. Deploy using either `render.yaml`, `render-stable.yaml`, or `render-docker.yaml`
2. Check the health endpoints:
   - Frontend: `https://your-frontend-service.onrender.com`
   - Backend: `https://your-backend-service.onrender.com`
   - Whisper: `https://your-whisper-service.onrender.com/health`
3. Test with a small audio file (< 5MB)
4. Monitor logs for any errors

## Troubleshooting

If you still encounter issues:

1. **Python __version__ KeyError**:
   - Try `render-stable.yaml` with conservative versions
   - Use `requirements-minimal.txt` for essential packages only
   - Check that setuptools and wheel are up to date
   - Try Docker approach for better isolation

2. **Frontend Build Issues**: 
   - Check that all dependencies are compatible
   - Try using `npm ci` instead of `npm install`
   - Ensure Node.js version is compatible

3. **Memory Issues**: Try the Docker approach which has better memory management
4. **ffmpeg Errors**: Check that build.sh is being executed properly
5. **Model Loading**: The service will fallback to "tiny" model if "base" fails
6. **Timeouts**: Reduce audio file size or use shorter recordings

## Performance Notes

- Base model is ~1GB vs Small model ~2GB
- Tiny model is ~39MB (fallback option)
- File size limit: 5MB for Render free tier
- Processing time: ~30-60 seconds for 1-minute audio
- Frontend: Static site deployment for fast loading 