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

## Deployment Options

### Option 1: Standard Build (Recommended)
Use the updated `render.yaml` with the build script:
```yaml
buildCommand: chmod +x build.sh && ./build.sh
```

### Option 2: Docker Build (Alternative)
Use `render-docker.yaml` for Docker-based deployment:
```yaml
env: docker
dockerfilePath: ./Dockerfile
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

3. **build.sh**:
   - Installs ffmpeg and audio processing libraries
   - Installs Python dependencies

4. **Dockerfile**:
   - Alternative approach using Docker
   - Ensures all system dependencies are available

## Environment Variables Required

Make sure to set these in Render:
- `NOTION_TOKEN` (if using Notion integration)
- `NOTION_DATABASE_ID` (if using Notion integration)

## Testing the Deployment

1. Deploy using either `render.yaml` or `render-docker.yaml`
2. Check the health endpoint: `https://your-whisper-service.onrender.com/health`
3. Test with a small audio file (< 5MB)
4. Monitor logs for any errors

## Troubleshooting

If you still encounter issues:

1. **Memory Issues**: Try the Docker approach which has better memory management
2. **ffmpeg Errors**: Check that build.sh is being executed properly
3. **Model Loading**: The service will fallback to "tiny" model if "base" fails
4. **Timeouts**: Reduce audio file size or use shorter recordings

## Performance Notes

- Base model is ~1GB vs Small model ~2GB
- Tiny model is ~39MB (fallback option)
- File size limit: 5MB for Render free tier
- Processing time: ~30-60 seconds for 1-minute audio 