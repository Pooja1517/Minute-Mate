# Whisper API Usage Guide

## ✅ What This Service Does

1. **Audio Transcription**: Converts audio files to text
2. **Notion Export**: Saves transcripts directly to Notion
3. **Google Docs Export**: Provides formatted text for Google Docs

## 🚀 How to Use

### Step 1: Deploy the Service

Follow the exact deployment steps I provided earlier to create the `minute-mate-whisper-minimal` service on Render.

### Step 2: Set Environment Variables

In your Render service, add these environment variables:

**For Notion Integration:**
- `NOTION_TOKEN` = Your Notion integration token
- `NOTION_DATABASE_ID` = Your Notion database ID

**For General Settings:**
- `PYTHONUNBUFFERED` = `1`
- `FLASK_ENV` = `production`

### Step 3: Test the Service

**Health Check:**
```
GET https://your-whisper-service.onrender.com/health
```

**Expected Response:**
```json
{
  "status": "ok",
  "whisper_model_loaded": true,
  "model_type": "tiny",
  "notion_available": true
}
```

## 📝 API Endpoints

### 1. Transcribe Audio
```
POST https://your-whisper-service.onrender.com/transcribe
```

**Request:**
- Content-Type: `multipart/form-data`
- Body: `audio` file (max 3MB)

**Response:**
```json
{
  "text": "Your transcribed text here..."
}
```

### 2. Export to Notion
```
POST https://your-whisper-service.onrender.com/export/notion
```

**Request:**
```json
{
  "transcript": "Your transcribed text here...",
  "title": "Meeting Title"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Successfully exported to Notion!",
  "page_id": "notion-page-id"
}
```

### 3. Export to Google Docs
```
POST https://your-whisper-service.onrender.com/export/google-docs
```

**Request:**
```json
{
  "transcript": "Your transcribed text here...",
  "title": "Meeting Title"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Text formatted for Google Docs. Copy and paste into a new Google Doc.",
  "formatted_text": "# Meeting Title\n\n## Meeting Transcript\n\nYour text here...",
  "instructions": "Copy the formatted text above and paste it into a new Google Doc"
}
```

### 4. Test Notion Integration
```
GET https://your-whisper-service.onrender.com/test-notion
```

## 🔧 Frontend Integration

### Update Your Frontend Code

```javascript
// Update your frontend to use the new Whisper service
const WHISPER_URL = "https://your-whisper-service.onrender.com";

// Transcribe audio
async function transcribeAudio(audioFile) {
  const formData = new FormData();
  formData.append('audio', audioFile);
  
  const response = await fetch(`${WHISPER_URL}/transcribe`, {
    method: 'POST',
    body: formData
  });
  
  return await response.json();
}

// Export to Notion
async function exportToNotion(transcript, title) {
  const response = await fetch(`${WHISPER_URL}/export/notion`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      transcript: transcript,
      title: title
    })
  });
  
  return await response.json();
}

// Export to Google Docs
async function exportToGoogleDocs(transcript, title) {
  const response = await fetch(`${WHISPER_URL}/export/google-docs`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      transcript: transcript,
      title: title
    })
  });
  
  return await response.json();
}
```

## 📊 Performance & Limitations

### With Tiny Model:
- **Memory usage**: ~39MB
- **Processing time**: 15-30 seconds for 1-minute audio
- **File size limit**: 3MB
- **Accuracy**: Good for most use cases

### Supported Audio Formats:
- MP3, WAV, M4A, FLAC, etc.
- Any format supported by ffmpeg

## 🎯 Complete Workflow

1. **Record audio** in your frontend
2. **Send to Whisper service** for transcription
3. **Get transcribed text** back
4. **Export to Notion** (creates page in your database)
5. **Export to Google Docs** (get formatted text to copy)

## 🚨 Troubleshooting

### Common Issues:

1. **File too large**: Keep audio files under 3MB
2. **Notion not working**: Check your token and database ID
3. **Service not responding**: Check Render logs
4. **Transcription empty**: Try shorter audio or better quality

### Error Responses:
- `400`: Bad request (missing file, file too large)
- `500`: Server error (check logs)

## ✅ Success Indicators

You'll know everything is working when:
- ✅ Health endpoint returns OK
- ✅ Can transcribe small audio files
- ✅ Notion export creates pages in your database
- ✅ Google Docs export provides formatted text
- ✅ Frontend can connect and use all features

This service gives you exactly what you want: **audio transcription + Notion export + Google Docs export** in a minimal, Render-optimized package! 