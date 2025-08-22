import React, { useState, useRef } from "react";

// Use deployed backend URL for production
const API_BASE_URL = "https://minute-mate-backend.onrender.com";

const AudioRecorder = ({ onUploadComplete }) => {
  const [recording, setRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState(null);
  const [audioBlob, setAudioBlob] = useState(null);
  const [audioURL, setAudioURL] = useState("");
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const audioRef = useRef(null);
  const fileInputRef = useRef();

  // Start recording
  const startRecording = async () => {
    setSelectedFile(null);
    setAudioBlob(null);
    setAudioURL("");
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const recorder = new MediaRecorder(stream);
    let chunks = [];
    recorder.ondataavailable = (e) => {
      chunks.push(e.data);
    };
    recorder.onstop = () => {
      const blob = new Blob(chunks, { type: "audio/webm" });
      setAudioBlob(blob);
      const url = URL.createObjectURL(blob);
      setAudioURL(url);
      if (audioRef.current) audioRef.current.src = url;
    };
    recorder.start();
    setMediaRecorder(recorder);
    setRecording(true);
  };

  // Stop recording
  const stopRecording = () => {
    if (mediaRecorder) {
      mediaRecorder.stop();
      setRecording(false);
    }
  };

  // Handle file upload
  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setAudioBlob(null);
      setAudioURL(URL.createObjectURL(file));
      setSelectedFile(file);
    }
  };

  // Transcribe audio
  const handleTranscribe = async () => {
    setLoading(true);
    const formData = new FormData();
    if (audioBlob) {
      formData.append("audio", audioBlob, "recording.webm");
    } else if (selectedFile) {
      formData.append("audio", selectedFile);
    } else {
      alert("Please record or upload a file first.");
      setLoading(false);
      return;
    }
    try {
      console.log("Sending request to:", `${API_BASE_URL}/transcribe`);
      const res = await fetch(`${API_BASE_URL}/transcribe`, {
        method: "POST",
        body: formData,
      });
      
      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }
      
      const data = await res.json();
      console.log("Transcription result:", data);
      if (data.text) {
        onUploadComplete({ text: data.text });
      } else if (data.transcript) {
        onUploadComplete({ text: data.transcript });
      } else {
        onUploadComplete({ error: "No transcript received from backend." });
      }
    } catch (err) {
      console.error("Transcription error:", err);
      if (err.message.includes("Failed to fetch") || err.message.includes("NetworkError")) {
        onUploadComplete({ 
          error: "Cannot connect to backend server. Please make sure the backend is running on " + API_BASE_URL 
        });
      } else {
        onUploadComplete({ error: "Transcription failed: " + err.message });
      }
    } finally {
      setLoading(false);
    }
  };

  // Reset all
  const handleReset = () => {
    setRecording(false);
    setMediaRecorder(null);
    setAudioBlob(null);
    setAudioURL("");
    setSelectedFile(null);
    if (audioRef.current) audioRef.current.src = "";
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  return (
    <div className="backdrop-blur-lg bg-[#232042]/70 border border-[#3b2e5a] rounded-2xl shadow-2xl w-full max-w-lg mx-auto p-8">
      <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
        <span role="img" aria-label="mic">🎤</span> MinuteMate Recorder
      </h2>
      <div className="mb-4 flex gap-3">
        <button
          onClick={startRecording}
          className="px-4 py-2 rounded font-semibold shadow transition-colors duration-150 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-60 disabled:cursor-not-allowed bg-gradient-to-r from-green-400 to-green-600 text-white"
          disabled={recording}
        >
          Start Recording
        </button>
        <button
          onClick={stopRecording}
          className="px-4 py-2 rounded font-semibold shadow transition-colors duration-150 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-60 disabled:cursor-not-allowed bg-gradient-to-r from-red-400 to-red-600 text-white"
          disabled={!recording}
        >
          Stop Recording
        </button>
        <button
          className="px-4 py-2 rounded font-semibold shadow transition-colors duration-150 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-60 disabled:cursor-not-allowed bg-gray-500 text-white"
          onClick={handleReset}
        >
          Reset
        </button>
      </div>
      <div className="my-4">
        {audioURL && (
          <audio controls className="w-full" ref={audioRef} src={audioURL} />
        )}
      </div>
      <div className="mb-4 flex gap-2 items-center">
        <input
          type="file"
          accept="audio/*"
          onChange={handleFileUpload}
          ref={fileInputRef}
          className="flex-1 border rounded px-2 py-1 bg-[#18162c] text-white placeholder:text-gray-400"
        />
        <button
          onClick={handleTranscribe}
          disabled={loading || (!audioBlob && !selectedFile)}
          className="btn-primary"
        >
          {loading ? "Transcribing..." : "Transcribe"}
        </button>
      </div>
      <p className="text-xs text-gray-300 mt-2">You can either record a new meeting or upload an existing audio file. Preview before transcribing.</p>
    </div>
  );
};

export default AudioRecorder;
