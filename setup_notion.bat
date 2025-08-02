@echo off
echo ========================================
echo    MinuteMate - Notion Setup
echo ========================================
echo.

echo Please follow these steps to set up Notion integration:
echo.
echo 1. Go to: https://www.notion.so/my-integrations
echo 2. Click "New integration"
echo 3. Name it "MinuteMate Integration"
echo 4. Copy the Internal Integration Token (starts with secret_)
echo 5. Create a page in Notion and copy its ID from the URL
echo 6. Share the page with your integration
echo.
echo After completing the steps above, enter your details below:
echo.

set /p NOTION_TOKEN="Enter your Notion Integration Token: "
set /p NOTION_PAGE_ID="Enter your Notion Page ID: "

echo.
echo Updating server/.env file...

(
echo # Server Configuration
echo NODE_ENV=development
echo PORT=5000
echo.
echo # Google OAuth Configuration ^(optional^)
echo GOOGLE_CLIENT_ID=your-google-client-id-here
echo GOOGLE_CLIENT_SECRET=your-google-client-secret-here
echo FRONTEND_URL=http://localhost:3001
echo.
echo # Notion Configuration
echo NOTION_TOKEN=%NOTION_TOKEN%
echo NOTION_PARENT_PAGE_ID=%NOTION_PAGE_ID%
echo.
echo # Whisper API Configuration
echo WHISPER_API_URL=http://localhost:5001
) > server\.env

echo.
echo ✅ Notion configuration updated!
echo.
echo Your Notion integration is now configured.
echo Restart your services to apply the changes.
echo.
echo Press any key to continue...
pause >nul 