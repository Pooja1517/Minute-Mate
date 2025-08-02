import React, { useState, useEffect } from "react";

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "https://minute-mate-backend.onrender.com";

const TranscriptDashboard = ({ data }) => {
  const [exportStatus, setExportStatus] = useState("");

  // Check for OAuth callback on component mount
  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get('code');
    const tokens = urlParams.get('tokens');
    const error = urlParams.get('error');
    
    if (tokens) {
      // Handle OAuth callback with tokens
      try {
        const parsedTokens = JSON.parse(decodeURIComponent(tokens));
        console.log('Received OAuth tokens:', parsedTokens);
        
        if (parsedTokens.access_token) {
          localStorage.setItem('googleTokens', JSON.stringify(parsedTokens));
          setExportStatus('Google authentication successful! ✅');
          console.log('✅ Tokens stored successfully');
        } else {
          setExportStatus('Invalid tokens received ❌');
          console.error('Invalid tokens:', parsedTokens);
        }
        
        // Clean up URL
        window.history.replaceState({}, document.title, window.location.pathname);
      } catch (err) {
        console.error('Failed to parse tokens:', err);
        setExportStatus('Failed to parse Google tokens ❌');
        // Clean up URL
        window.history.replaceState({}, document.title, window.location.pathname);
      }
    } else if (code) {
      // Handle OAuth callback with code (legacy)
      handleOAuthCallback(code);
      // Clean up URL
      window.history.replaceState({}, document.title, window.location.pathname);
    } else if (error) {
      console.error('OAuth error:', error);
      setExportStatus('Google authentication failed ❌');
      // Clean up URL
      window.history.replaceState({}, document.title, window.location.pathname);
    }
  }, []);

  const handleOAuthCallback = async (code) => {
    try {
      const res = await fetch(`${API_BASE_URL}/auth/google/callback?code=${code}`);
      const { tokens } = await res.json();
      localStorage.setItem('googleTokens', JSON.stringify(tokens));
      setExportStatus('Google authentication successful! ✅');
    } catch (err) {
      setExportStatus('Google authentication failed ❌');
    }
  };

  const handleExportNotion = async () => {
    setExportStatus("Exporting to Notion...");
    try {
      const res = await fetch(`${API_BASE_URL}/export/notion`, {
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
        if (result.pageUrl) {
          setExportStatus(
            <span>
              Exported to Notion successfully ✅ -{' '}
              <a 
                href={result.pageUrl} 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-blue-400 hover:text-blue-300 underline"
              >
                View Page
              </a>
            </span>
          );
        } else {
          setExportStatus("Exported to Notion successfully ✅");
        }
      } else {
        if (result.setupInstructions) {
          setExportStatus(
            <span className="text-red-600">
              Notion Setup Required ❌ - {result.error}
              <br />
              <span className="text-sm text-gray-400 mt-1 block">
                {result.setupInstructions}
              </span>
            </span>
          );
        } else {
          setExportStatus("Failed to export to Notion ❌ - " + (result.error || result.details || "Unknown error"));
        }
      }
    } catch (err) {
      setExportStatus("Failed to export to Notion ❌ - Network error");
    }
  };

  // Google Docs OAuth and export logic
  const handleGoogleAuth = async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/auth/google`);
      const { url } = await res.json();
      window.location.href = url;
    } catch (err) {
      setExportStatus('Failed to start Google authentication ❌');
    }
  };

  const handleExportGoogleDocs = async () => {
    try {
      const tokensStr = localStorage.getItem('googleTokens');
      if (!tokensStr) {
        setExportStatus('Please sign in with Google first!');
        await handleGoogleAuth();
        return;
      }
      
      const tokens = JSON.parse(tokensStr);
      if (!tokens || !tokens.access_token) {
        setExportStatus('Invalid tokens. Please sign in again with Google.');
        localStorage.removeItem('googleTokens');
        await handleGoogleAuth();
        return;
      }
      
      // Check if token is expired
      if (tokens.expiry_date && Date.now() > tokens.expiry_date) {
        setExportStatus('Token expired. Please sign in again with Google.');
        localStorage.removeItem('googleTokens');
        await handleGoogleAuth();
        return;
      }
      
      setExportStatus('Exporting to Google Docs...');
      
      const res = await fetch(`${API_BASE_URL}/export/googledocs`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ summary: data.summary, actions: data.actions, tokens }),
      });
      
      const result = await res.json();
      
      if (result.success) {
        const docUrl = result.docUrl || `https://docs.google.com/document/d/${result.docId}/edit`;
        setExportStatus(
          <span>
            Exported to Google Docs! ✅{' '}
            <a 
              href={docUrl} 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-blue-400 hover:text-blue-300 underline"
            >
              View Document
            </a>
          </span>
        );
      } else {
        if (result.error && result.error.includes('sign in again')) {
          // Clear invalid tokens and prompt for re-authentication
          localStorage.removeItem('googleTokens');
          setExportStatus('Authentication failed. Please sign in again with Google.');
          await handleGoogleAuth();
        } else {
          setExportStatus('Failed to export to Google Docs: ' + (result.error || 'Unknown error'));
        }
      }
    } catch (err) {
      console.error('Google Docs export error:', err);
      setExportStatus('Failed to export to Google Docs ❌');
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
            <button 
              className="btn bg-blue-700 hover:bg-blue-800" 
              onClick={handleExportGoogleDocs}
              title="Export to Google Docs"
            >
              📄 Export to Google Docs
            </button>
          </div>
          {exportStatus && (
            <div className={`font-medium mt-2 ${
              typeof exportStatus === 'string' && exportStatus.includes('successfully') 
                ? 'text-green-600' 
                : typeof exportStatus === 'string' && exportStatus.includes('❌') 
                ? 'text-red-600' 
                : 'text-green-600'
            }`}>
              {exportStatus}
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default TranscriptDashboard;
