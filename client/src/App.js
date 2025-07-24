import React, { useState } from "react";
import AudioRecorder from "./components/AudioRecorder";
import TranscriptDashboard from "./components/TranscriptDashboard";
import "./index.css";

function App() {
  const [result, setResult] = useState(null);

  return (
    <div className="min-h-screen flex flex-col items-center justify-center">
      <div className="mt-8 mb-4 text-center">
        <div className="app-title">Minute <span className="text-pink-400">Mate</span></div>
        <div className="app-subtitle">AI-powered meeting assistant</div>
      </div>
      <div className="card flex flex-col md:flex-row items-center justify-center gap-8 p-10">
        <img src="/robot2.jpg" alt="Robot" className="w-[320px] h-[320px] object-cover rounded-xl shadow-lg" />
        <div className="flex-1 w-full max-w-lg flex flex-col items-center justify-center">
          <AudioRecorder onUploadComplete={setResult} />
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
