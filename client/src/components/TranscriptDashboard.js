import React, { useState } from "react";

const TranscriptDashboard = ({ data }) => {
  const [exportStatus, setExportStatus] = useState("");

  const handleExportNotion = async () => {
    setExportStatus("Exporting to Notion...");
    try {
      const res = await fetch("http://localhost:5000/export/notion", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          transcript: data.transcript,
          summary: data.summary,
          actions: data.actions,
        }),
      });
      const result = await res.json();
      if (result.success) {
        setExportStatus("Exported to Notion successfully ✅");
      } else {
        setExportStatus("Failed to export to Notion ❌");
      }
    } catch (err) {
      setExportStatus("Failed to export to Notion ❌");
    }
  };
  const handleExportGoogle = async () => {
    setExportStatus("Exporting to Google Docs...");
    try {
      const res = await fetch("http://localhost:5000/export/googledocs", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          transcript: data.transcript,
          summary: data.summary,
          actions: data.actions,
        }),
      });
      const result = await res.json();
      if (result.success) {
        setExportStatus("Exported to Google Docs successfully ✅");
      } else {
        setExportStatus("Failed to export to Google Docs ❌");
      }
    } catch (err) {
      setExportStatus("Failed to export to Google Docs ❌");
    }
  };

  return (
    <div className="p-4 border rounded-xl mt-4 bg-[#232042] bg-opacity-90 shadow">
      <h3 className="text-lg font-bold mb-2">📄 Transcription Result</h3>
      {data.error ? (
        <p className="text-red-600">❌ {data.error}</p>
      ) : (
        <>
          <h4 className="font-semibold">📝 Transcript:</h4>
          <p className="mb-4 whitespace-pre-line">{data.transcript}</p>

          <h4 className="font-semibold">🧠 Summary:</h4>
          <p className="mb-4 whitespace-pre-line">{data.summary}</p>

          <h4 className="font-semibold">✅ Action Items:</h4>
          <ul className="list-disc pl-6 mb-4">
            {data.actions?.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>

          <div className="flex gap-3 mb-2">
            <button className="btn bg-black hover:bg-gray-800" onClick={handleExportNotion}>
              🗂 Export to Notion
            </button>
            <button className="btn bg-blue-700 hover:bg-blue-800" onClick={handleExportGoogle}>
              📄 Export to Google Docs
            </button>
          </div>
          {exportStatus && <div className={`font-medium mt-2 ${exportStatus.includes('successfully') ? 'text-green-600' : 'text-red-600'}`}>{exportStatus}</div>}
        </>
      )}
    </div>
  );
};

export default TranscriptDashboard;
