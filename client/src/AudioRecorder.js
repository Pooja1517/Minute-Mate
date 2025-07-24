import React, { useState, useRef } from "react";

const AudioRecorder = () => {
  const [audioBlob, setAudioBlob] = useState(null);
  const [audioURL, setAudioURL] = useState("");
  const [transcript, setTranscript] = useState("");
  const [loading, setLoading] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [mediaRecorder, setMediaRecorder] = useState(null);
  const [status, setStatus] = useState("stopped");
  const fileInputRef = useRef();
  const chunksRef = useRef([]);

  const startRecording = async () => {
    setSelectedFile(null);
    setAudioBlob(null);
    setTranscript("");
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const recorder = new window.MediaRecorder(stream);
    recorder.ondataavailable = (e) => chunksRef.current.push(e.data);
    recorder.onstop = () => {
      const blob = new Blob(chunksRef.current, { type: "audio/webm" });
      setAudioBlob(blob);
      setAudioURL(URL.createObjectURL(blob));
      chunksRef.current = [];
    };
    recorder.start();
    setMediaRecorder(recorder);
    setStatus("recording");
  };

  const pauseRecording = () => {
    if (mediaRecorder && mediaRecorder.state === "recording") {
      mediaRecorder.pause();
      setStatus("paused");
    }
  };

  const resumeRecording = () => {
    if (mediaRecorder && mediaRecorder.state === "paused") {
      mediaRecorder.resume();
      setStatus("recording");
    }
  };

  const stopRecording = () => {
    if (mediaRecorder) {
      mediaRecorder.stop();
      setStatus("stopped");
    }
  };

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setAudioBlob(null);
      setAudioURL(URL.createObjectURL(file));
      setSelectedFile(file);
      setTranscript("");
    }
  };

  const handleTranscribe = async () => {
    const formData = new FormData();
    if (audioBlob) {
      formData.append("audio", new File([audioBlob], "recording.webm", { type: "audio/webm" }));
    } else if (selectedFile) {
      formData.append("audio", selectedFile);
    } else {
      alert("Please record or upload a file.");
      return;
    }
    setLoading(true);
    try {
      const res = await fetch("http://localhost:5000/transcribe", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      if (res.ok && data.text) {
        setTranscript(data.text);
      } else if (res.status === 400) {
        setTranscript("No audio file received by backend. Please try again with a different file or recording.");
      } else if (res.status === 401) {
        setTranscript("Unauthorized: Check your OpenAI API key in the backend.");
      } else {
        setTranscript("Transcription failed. " + (data.error || ""));
        console.error("Transcription error:", data);
      }
    } catch (err) {
      setTranscript(
        "Meeting Title: Project Kickoff\nParticipants: Alice, Bob, Carol\n\nKey Points:\n- Discussed project goals and deliverables\n- Set deadlines for initial milestones\n- Assigned roles to team members\n\nDecisions Made:\n- Project will start on July 20th\n- Weekly sync meetings every Monday\n\nAction Items:\n- Alice: Prepare project plan by July 18th\n- Bob: Set up repository by July 19th\n- Carol: Draft initial requirements by July 21st\n\n[Sample transcript shown due to backend error]"
      );
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white p-6 rounded shadow w-full max-w-lg mx-auto mt-10">
      <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
        🎤 MinuteMate Recorder
      </h2>
      <div className="mb-4 flex gap-2">
        <button
          onClick={startRecording}
          className="bg-green-500 text-white px-4 py-2 rounded"
        >
          Start
        </button>
        <button
          onClick={pauseRecording}
          className="bg-yellow-500 text-white px-4 py-2 rounded"
        >
          Pause
        </button>
        <button
          onClick={resumeRecording}
          className="bg-blue-500 text-white px-4 py-2 rounded"
        >
          Resume
        </button>
        <button
          onClick={stopRecording}
          className="bg-red-500 text-white px-4 py-2 rounded"
        >
          Stop
        </button>
      </div>
      <div className="my-4">
        <audio src={audioURL} controls className="w-full" />
      </div>
      <div className="mb-4 flex gap-2 items-center">
        <input
          type="file"
          accept="audio/*"
          onChange={handleFileUpload}
          ref={fileInputRef}
          className="flex-1"
        />
        <button
          onClick={handleTranscribe}
          disabled={loading}
          className="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700"
        >
          {loading ? "Transcribing..." : "Transcribe Audio"}
        </button>
      </div>
      {transcript && (
        <div className="mt-4 bg-gray-100 p-3 rounded">
          <strong>📝 Transcript:</strong>
          <p className="mt-2">{transcript}</p>
        </div>
      )}
    </div>
  );
};

export default AudioRecorder;