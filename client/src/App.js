import React, { useState } from "react";
import AudioRecorder from "./components/AudioRecorder";
import TranscriptDashboard from "./components/TranscriptDashboard";
import "./index.css";

function App() {
  const [result, setResult] = useState(null);

  // New: Call summarization after transcription
  const handleUploadComplete = async (data) => {
    if (data.text) {
      // If transcript is present, call summarize endpoint
      console.log("Transcription complete, sending to summarize:", data.text);
      try {
        const res = await fetch("http://localhost:5001/summarize", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ transcript: data.text }),
        });
        const ai = await res.json();
        console.log("Summarize response:", ai);
        if (res.ok && ai.summary) {
          setResult({ transcript: data.text, summary: ai.summary, actions: ai.action_items });
        } else if (ai.error) {
          setResult({ transcript: data.text, summary: "(Failed to summarize)", actions: [], error: ai.error });
        } else {
          setResult({ transcript: data.text, summary: "(No summary returned)", actions: [] });
        }
      } catch (err) {
        setResult({ transcript: data.text, summary: "(Failed to summarize)", actions: [], error: err.message });
      }
    } else {
      setResult(data);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center">
      <div className="mt-8 mb-4 text-center">
        <div className="app-title">Minute <span className="text-pink-400">Mate</span></div>
        <div className="app-subtitle">AI-powered meeting assistant</div>
      </div>
      <div className="card flex flex-col md:flex-row items-center justify-center gap-8 p-10">
        <img src="/robot2.jpg" alt="Robot" className="w-[320px] h-[320px] object-cover rounded-xl shadow-lg" />
        <div className="flex-1 w-full max-w-lg flex flex-col items-center justify-center">
          <AudioRecorder onUploadComplete={handleUploadComplete} />
        </div>
      </div>
      {result && (
        <div className="mt-8 w-full max-w-3xl">
          <div className="bg-[#232042] bg-opacity-90 rounded-3xl shadow-2xl p-8">
            <TranscriptDashboard data={result} />
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
