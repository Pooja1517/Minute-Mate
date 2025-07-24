# MinuteMate

AI-powered meeting assistant for recording, transcribing, and summarizing meetings.

---

## 🚀 Features
- **Record or upload meeting audio** (web UI)
- **Transcribe audio** using local OpenAI Whisper (free, accurate, no API key needed)
- **View transcript, summary, and action items**
- **Export to Notion or Google Docs** (stub endpoints)
- **Modern, beautiful UI** with robot mascot

---

## 🛠️ Tech Stack
- **Frontend:** React, Tailwind CSS
- **Backend:** Node.js, Express, Multer
- **Transcription:** Python, Flask, OpenAI Whisper (local)
- **Audio Processing:** ffmpeg

---

## ⚡ Setup Instructions

### 1. Clone the Repository
```sh
git clone https://github.com/Pooja1517/Minute-Mate.git
cd minutemate
```

### 2. Install Node.js Dependencies
```sh
cd client
npm install
cd ../server
npm install
```

### 3. Install Python & Whisper Dependencies
- Install [Python 3.10+](https://www.python.org/downloads/)
- Install [ffmpeg](https://www.gyan.dev/ffmpeg/builds/) and add to PATH
- Install Python packages:
```sh
pip install flask torch git+https://github.com/openai/whisper.git
```

### 4. Start the Whisper Flask Server
```sh
python whisper_api.py
```
- Make sure you see `Running on http://127.0.0.1:5001` in the terminal.

### 5. Start the Node.js Backend
```sh
cd server
node index.js
```
- Should show `🚀 Server running on http://localhost:5000`

### 6. Start the React Frontend
```sh
cd ../client
npm start
```
- App will open at [http://localhost:3000](http://localhost:3000)

---

## 📝 Usage
1. **Record or upload** an audio file in the web UI.
2. **Click Transcribe** to get the transcript (processed locally by Whisper).
3. **View transcript, summary, and action items** in the dashboard.
4. **Export** to Notion or Google Docs (stub endpoints for now).

---

## 📦 Notes
- No API key or cloud usage required for transcription (Whisper runs locally).
- Make sure ffmpeg is installed and in your PATH for Whisper to work.
- For best results, use clear audio in mp3, wav, or m4a format.

---

## 📸 Sample Screenshot
![screenshot](client/public/Screenshot.png)

---

## 🤖 Credits
- Robot image: Your provided asset
- UI inspired by devchallenges.io
- Built with ❤️ by Pooja Galigoudar
