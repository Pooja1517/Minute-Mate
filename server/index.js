require('dotenv').config();
const express = require("express");
const multer = require("multer");
const cors = require("cors");
const path = require("path");
const fs = require("fs");
const { transcribeAudio } = require("./whisperService");
const { google } = require('googleapis');
const { Client } = require('@notionhq/client');

const app = express();
const upload = multer({ dest: "uploads/" });

app.use(cors());
app.use(express.json());

// Health check endpoint
app.get("/health", (req, res) => {
  res.json({ 
    status: "healthy", 
    service: "minute-mate-backend",
    environment: process.env.RENDER ? "production" : "development",
    timestamp: new Date().toISOString()
  });
});

app.post("/transcribe", upload.single("audio"), async (req, res) => {
  console.log("=== Transcription Request Received ===");
  console.log("Request headers:", req.headers);
  console.log("Request body keys:", Object.keys(req.body || {}));
  
  if (!req.file) {
    console.log("No file received! req.body:", req.body);
    return res.status(400).json({ error: "No audio file uploaded" });
  }
  
  console.log("Received file:", req.file.originalname, req.file.mimetype, req.file.size);
  const filePath = path.resolve(req.file.path);
  
  try {
    console.log("Starting transcription...");
    const result = await transcribeAudio(filePath);
    
    // Clean up file
    if (fs.existsSync(filePath)) {
      fs.unlinkSync(filePath);
      console.log("Temporary file cleaned up");
    }
    
    if (!result || !result.transcript) {
      console.error("No transcript in result:", result);
      return res.status(500).json({ error: "Transcription failed or returned empty result." });
    }
    
    console.log("Transcription completed successfully, length:", result.transcript.length);
    res.json(result);
  } catch (error) {
    // Clean up file on error
    if (fs.existsSync(filePath)) {
      try {
        fs.unlinkSync(filePath);
        console.log("Temporary file cleaned up after error");
      } catch (cleanupError) {
        console.error("Error cleaning up file:", cleanupError);
      }
    }
    
    console.error("Transcription error:", error.message);
    console.error("Error stack:", error.stack);
    res.status(500).json({ error: error.message || "Transcription error" });
  }
});

// Google OAuth2 setup
const credentials = {
  "web": {
    "client_id": process.env.GOOGLE_CLIENT_ID || "your-google-client-id-here",
    "project_id": "minutemate-467409",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": process.env.GOOGLE_CLIENT_SECRET || "your-google-client-secret-here",
    "redirect_uris": [process.env.GOOGLE_REDIRECT_URI || "https://minute-mate.onrender.com/auth/google/callback"]
  }
};
const { client_id, client_secret, redirect_uris } = credentials.web;
const oAuth2Client = new google.auth.OAuth2(client_id, client_secret, redirect_uris[0]);

// Step 1: Get Auth URL (frontend should redirect user to this)
app.get('/auth/google', (req, res) => {
  const authUrl = oAuth2Client.generateAuthUrl({
    access_type: 'offline',
    scope: ['https://www.googleapis.com/auth/documents'],
    prompt: 'consent', // Force consent to get refresh token
  });
  res.json({ url: authUrl });
});

// Step 2: Handle OAuth2 callback and get tokens
app.get('/auth/google/callback', async (req, res) => {
  const code = req.query.code;
  try {
    const { tokens } = await oAuth2Client.getToken(code);
    console.log('Received tokens:', tokens);
    
    // Check if we got a refresh token
    if (!tokens.refresh_token) {
      console.warn('No refresh token received. This might cause issues.');
    }
    
    oAuth2Client.setCredentials(tokens);
    
    // Redirect back to frontend with tokens
    const tokenParam = encodeURIComponent(JSON.stringify(tokens));
    const frontendUrl = process.env.FRONTEND_URL || "https://minute-mate-omega.vercel.app";
    res.redirect(`${frontendUrl}?tokens=${tokenParam}`);
  } catch (error) {
    console.error('OAuth callback error:', error);
    const frontendUrl = process.env.FRONTEND_URL || "https://minute-mate-omega.vercel.app";
    res.redirect(`${frontendUrl}?error=oauth_failed`);
  }
});

// Step 3: Export to Google Docs
app.post('/export/googledocs', async (req, res) => {
  const { summary, actions, tokens } = req.body;
  console.log('Received tokens:', tokens);
  console.log('Summary:', summary);
  console.log('Actions:', actions);
  
  if (!tokens || !tokens.access_token) {
    console.error('Missing tokens in request:', { hasTokens: !!tokens, hasAccessToken: !!(tokens && tokens.access_token) });
    return res.status(400).json({ error: 'Missing or invalid Google OAuth tokens. Please sign in again.' });
  }
  
  try {
    oAuth2Client.setCredentials(tokens);

    const docs = google.docs({ version: 'v1', auth: oAuth2Client });
    
    // Create the document
    const doc = await docs.documents.create({
      requestBody: {
        title: 'Meeting Notes',
      }
    });
    
    const documentId = doc.data.documentId;
    console.log('Created document with ID:', documentId);
    
    // Add content to the document
    const requests = [
      {
        insertText: {
          location: {
            index: 1
          },
          text: 'Meeting Notes\n\n'
        }
      },
      {
        insertText: {
          location: {
            index: 15
          },
          text: 'Summary:\n'
        }
      },
      {
        insertText: {
          location: {
            index: 25
          },
          text: summary + '\n\n'
        }
      },
      {
        insertText: {
          location: {
            index: 25 + summary.length + 2
          },
          text: 'Action Items:\n'
        }
      }
    ];
    
    // Add action items
    if (actions && actions.length > 0) {
      actions.forEach((action, index) => {
        requests.push({
          insertText: {
            location: {
              index: 25 + summary.length + 15 + (index * 2)
            },
            text: `• ${action}\n`
          }
        });
      });
    }
    
    // Apply the formatting requests
    await docs.documents.batchUpdate({
      documentId: documentId,
      requestBody: {
        requests: requests
      }
    });
    
    console.log('Document content added successfully');
    const docUrl = `https://docs.google.com/document/d/${documentId}/edit`;
    res.json({ success: true, docId: documentId, docUrl: docUrl });
    
  } catch (error) {
    console.error('Google Docs export error:', error);
    res.status(500).json({ error: error.message || 'Failed to export to Google Docs' });
  }
});

// Notion client setup
const notion = new Client({
  auth: process.env.NOTION_TOKEN || 'your-notion-integration-token-here',
});

// Export to Notion
app.post("/export/notion", async (req, res) => {
  const { transcript, summary, actions } = req.body;
  
  if (!transcript && !summary && !actions) {
    return res.status(400).json({ error: "No data provided" });
  }

  // Check if Notion is properly configured
  const notionToken = process.env.NOTION_TOKEN;
  const notionPageId = process.env.NOTION_PARENT_PAGE_ID;
  
  if (!notionToken || notionToken === 'your-notion-integration-token-here') {
    return res.status(400).json({ 
      error: "Notion integration not configured. Please set up NOTION_TOKEN in your .env file.",
      setupInstructions: "To set up Notion: 1) Create a Notion integration at https://www.notion.so/my-integrations 2) Get your integration token 3) Add it to server/.env as NOTION_TOKEN=your_token_here"
    });
  }
  
  if (!notionPageId || notionPageId === 'your-parent-page-id-here') {
    return res.status(400).json({ 
      error: "Notion page ID not configured. Please set up NOTION_PARENT_PAGE_ID in your .env file.",
      setupInstructions: "To set up Notion page: 1) Create a page in Notion 2) Share it with your integration 3) Copy the page ID from the URL 4) Add it to server/.env as NOTION_PARENT_PAGE_ID=your_page_id_here"
    });
  }

  try {
    // Create a new page in Notion
    const response = await notion.pages.create({
      parent: {
        type: "page_id",
        page_id: notionPageId,
      },
      properties: {
        title: {
          title: [
            {
              text: {
                content: `Meeting Notes - ${new Date().toLocaleDateString()}`,
              },
            },
          ],
        },
      },
      children: [
        {
          object: "block",
          type: "heading_2",
          heading_2: {
            rich_text: [
              {
                text: {
                  content: "📝 Transcript",
                },
              },
            ],
          },
        },
        {
          object: "block",
          type: "paragraph",
          paragraph: {
            rich_text: [
              {
                text: {
                  content: transcript || "No transcript available",
                },
              },
            ],
          },
        },
        {
          object: "block",
          type: "heading_2",
          heading_2: {
            rich_text: [
              {
                text: {
                  content: "🧠 Summary",
                },
              },
            ],
          },
        },
        {
          object: "block",
          type: "paragraph",
          paragraph: {
            rich_text: [
              {
                text: {
                  content: summary || "No summary available",
                },
              },
            ],
          },
        },
        {
          object: "block",
          type: "heading_2",
          heading_2: {
            rich_text: [
              {
                text: {
                  content: "✅ Action Items",
                },
              },
            ],
          },
        },
        ...(actions && actions.length > 0 ? actions.map(action => ({
          object: "block",
          type: "to_do",
          to_do: {
            rich_text: [
              {
                text: {
                  content: action,
                },
              },
            ],
            checked: false,
          },
        })) : [{
          object: "block",
          type: "paragraph",
          paragraph: {
            rich_text: [
              {
                text: {
                  content: "No action items identified",
                },
              },
            ],
          },
        }]),
      ],
    });

    res.json({ 
      success: true, 
      message: "Exported to Notion successfully!",
      pageId: response.id,
      pageUrl: `https://notion.so/${response.id.replace(/-/g, '')}`
    });
  } catch (error) {
    console.error('Notion export error:', error);
    res.status(500).json({ 
      success: false, 
      error: error.message || "Failed to export to Notion",
      details: "Check that your Notion integration token is valid and the page ID exists"
    });
  }
});

app.listen(5000, () => console.log("🚀 Server running on http://localhost:5000"));
