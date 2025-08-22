const fs = require("fs");
const axios = require("axios");
const FormData = require("form-data");

const transcribeAudio = async (filePath) => {
  const form = new FormData();
  form.append("audio", fs.createReadStream(filePath));
  
  // Automatic environment detection
  // Check if running on Render (production) or localhost (development)
  const isProduction = process.env.RENDER || process.env.NODE_ENV === 'production';
  const whisperApiUrl = isProduction 
    ? (process.env.WHISPER_API_URL || "https://minute-mate-whisper.onrender.com")
    : "http://127.0.0.1:5001";
  
  console.log(`Connecting to Whisper API at: ${whisperApiUrl}`);
  console.log(`File path: ${filePath}`);
  console.log(`Form headers:`, form.getHeaders());
  
  try {
    const response = await axios.post(
      `${whisperApiUrl}/transcribe`,
      form,
      { 
        headers: form.getHeaders(),
        timeout: 300000, // 5 minute timeout for very large files
        maxContentLength: 50 * 1024 * 1024 // 50MB max file size
      }
    );
    
    if (!response.data || !response.data.text) {
      throw new Error('Invalid response from Whisper API: No transcript text received');
    }
    
    return { transcript: response.data.text };
  } catch (error) {
    console.error('Whisper API Error:', error.message);
    
    if (error.code === 'ECONNREFUSED') {
      throw new Error(`Cannot connect to Whisper API at ${whisperApiUrl}. Please check if the service is running.`);
    } else if (error.code === 'ETIMEDOUT') {
      throw new Error('Whisper API request timed out. Please try again.');
    } else if (error.response) {
      throw new Error(`Whisper API error: ${error.response.status} - ${error.response.data?.error || error.response.statusText}`);
    } else {
      throw new Error(`Whisper API error: ${error.message}`);
    }
  }
};

module.exports = { transcribeAudio }; 