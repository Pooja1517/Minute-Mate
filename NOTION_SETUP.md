# Notion Integration Setup Guide

## Step 1: Create a Notion Integration

1. **Go to [Notion Integrations](https://www.notion.so/my-integrations)**
2. **Click "New integration"**
3. **Fill in the details:**
   - Name: "Minute Mate"
   - Associated workspace: Choose your workspace
   - Capabilities: Select "Read content" and "Update content"
4. **Click "Submit"**
5. **Copy the "Internal Integration Token"** (starts with `secret_`)

## Step 2: Create a Notion Page

1. **Go to [Notion](https://www.notion.so)**
2. **Create a new page** (or use an existing one)
3. **Click the "Share" button** in the top right
4. **Click "Invite"** and search for your integration name ("Minute Mate")
5. **Add the integration** to the page
6. **Copy the page ID** from the URL:
   - URL format: `https://www.notion.so/Page-Title-1234567890abcdef1234567890abcdef`
   - Page ID: `1234567890abcdef1234567890abcdef`

## Step 3: Update Your .env File

1. **Open `server/.env`**
2. **Add these lines:**
   ```
   NOTION_TOKEN=secret_your_integration_token_here
   NOTION_PARENT_PAGE_ID=your_page_id_here
   ```
3. **Replace with your actual values**

## Step 4: Restart Your Server

1. **Stop your server** (Ctrl+C)
2. **Start it again:** `node index.js`

## Step 5: Test

1. **Go to your app** (`http://localhost:3000`)
2. **Try the Notion export** - it should now work!

## Troubleshooting

- **"Invalid token"**: Make sure you copied the full token starting with `secret_`
- **"Page not found"**: Make sure the page ID is correct and the integration has access
- **"Permission denied"**: Make sure you added the integration to the page

## Example .env File

```
# Google OAuth2 Credentials
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret

# Notion Configuration
NOTION_TOKEN=secret_abc123def456ghi789jkl012mno345pqr678stu901vwx234yz
NOTION_PARENT_PAGE_ID=1234567890abcdef1234567890abcdef
``` 