# Notion Integration Setup Guide

This guide will help you set up Notion integration for MinuteMate so you can export your meeting notes directly to Notion.

## 📋 Prerequisites

- A Notion account
- Access to create integrations
- A Notion page where you want to store meeting notes

## 🔧 Step-by-Step Setup

### Step 1: Create Notion Integration

1. **Go to Notion Integrations**: https://www.notion.so/my-integrations
2. **Click "New integration"**
3. **Fill in the integration details:**
   - **Name**: `MinuteMate Integration` (or any name you prefer)
   - **Associated workspace**: Select your workspace
   - **Capabilities**: 
     - ✅ **Read content**
     - ✅ **Update content**
     - ✅ **Insert content**
4. **Click "Submit"**
5. **Copy the "Internal Integration Token"** (it starts with `secret_`)

### Step 2: Create a Notion Page

1. **Open Notion** and navigate to your workspace
2. **Create a new page** (not a database)
3. **Name it** something like "Meeting Notes" or "MinuteMate Exports"
4. **Copy the page ID** from the URL:
   - URL format: `https://notion.so/your-page-id-here`
   - The page ID is the part after the last `/`
   - Example: If URL is `https://notion.so/abc123def456`, the page ID is `abc123def456`

### Step 3: Share the Page with Your Integration

1. **Open the page you created**
2. **Click "Share"** in the top right corner
3. **Click "Invite"**
4. **Search for your integration name** (e.g., "MinuteMate Integration")
5. **Select it and click "Invite"**
6. **Give it "Full access"** permissions

### Step 4: Update Your Environment Configuration

#### Option A: Use the Setup Script (Recommended)

Run one of these commands in your project directory:

**Windows Batch:**
```cmd
.\setup_notion.bat
```

**PowerShell:**
```powershell
.\setup_notion.ps1
```

#### Option B: Manual Configuration

Edit `server/.env` file and update these lines:

```env
NOTION_TOKEN=secret_your_actual_token_here
NOTION_PARENT_PAGE_ID=your_actual_page_id_here
```

### Step 5: Restart Your Services

After updating the configuration, restart your services:

```cmd
.\FINAL_FIX.bat
```

## 🧪 Testing the Integration

1. **Start your services** using the startup script
2. **Open** http://localhost:3001 in your browser
3. **Record or upload** an audio file
4. **Transcribe** the audio
5. **Click "Export to Notion"**
6. **Check your Notion page** - you should see a new page with your meeting notes

## 📝 What Gets Exported to Notion

When you export to Notion, MinuteMate creates a new page with:

- **Meeting Summary** - Bullet points of key points
- **Action Items** - Tasks and follow-ups as checkboxes
- **Full Transcript** - Complete meeting transcript (collapsed by default)

## 🔍 Troubleshooting

### "Notion integration not configured"
- Make sure you've updated the `server/.env` file
- Restart your services after making changes
- Check that the token starts with `secret_`

### "Failed to export to Notion"
- Verify the page ID is correct
- Make sure you've shared the page with your integration
- Check that the integration has "Full access" permissions

### "Page not found"
- Ensure the page ID is correct (copy from the URL)
- Make sure the page exists and is accessible
- Verify the integration has access to the page

## 🔐 Security Notes

- Keep your Notion integration token secure
- Don't share your `.env` file publicly
- The token gives access to pages shared with the integration

## 📞 Support

If you encounter issues:

1. **Check the Notion integration page** for any error messages
2. **Verify your page permissions** in Notion
3. **Restart your services** after configuration changes
4. **Check the browser console** for any error messages

## ✅ Success Indicators

You'll know the setup is working when:

- ✅ No "Notion Setup Required" error appears
- ✅ "Export to Notion" button works without errors
- ✅ New pages appear in your Notion workspace
- ✅ Meeting notes are properly formatted in Notion 