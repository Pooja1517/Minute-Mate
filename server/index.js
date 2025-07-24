const express = require("express");
const multer = require("multer");
const cors = require("cors");
const path = require("path");
const fs = require("fs");
const { transcribeAudio } = require("./whisperService");

const app = express();
const upload = multer({ dest: "uploads/" });

app.use(cors());
app.use(express.json());

app.post("/transcribe", upload.single("audio"), async (req, res) => {
  if (!req.file) {
    console.log("No file received! req.body:", req.body);
    return res.status(400).json({ error: "No audio file uploaded" });
  }
  console.log("Received file:", req.file.originalname, req.file.mimetype, req.file.size);
  const filePath = path.resolve(req.file.path);
  try {
    const result = await transcribeAudio(filePath);
    fs.unlinkSync(filePath); // delete file after processing
    if (!result || !result.transcript) {
      return res.status(500).json({ error: "Transcription failed or returned empty result." });
    }
    res.json(result);
  } catch (error) {
    if (fs.existsSync(filePath)) fs.unlinkSync(filePath);
    res.status(500).json({ error: error.message || "Transcription error" });
  }
});

// Export to Notion (stub)
app.post("/export/notion", async (req, res) => {
  const { transcript, summary, actions } = req.body;
  if (!transcript && !summary && !actions) {
    return res.status(400).json({ error: "No data provided" });
  }
  res.json({ success: true, message: "Exported to Notion (stub)" });
});

// Export to Google Docs (stub)
app.post("/export/googledocs", async (req, res) => {
  const { transcript, summary, actions } = req.body;
  if (!transcript && !summary && !actions) {
    return res.status(400).json({ error: "No data provided" });
  }
  res.json({ success: true, message: "Exported to Google Docs (stub)" });
});

app.listen(5000, () => console.log("🚀 Server running on http://localhost:5000"));
