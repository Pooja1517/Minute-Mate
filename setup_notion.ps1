Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    MinuteMate - Notion Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Please follow these steps to set up Notion integration:" -ForegroundColor White
Write-Host ""
Write-Host "1. Go to: https://www.notion.so/my-integrations" -ForegroundColor Yellow
Write-Host "2. Click 'New integration'" -ForegroundColor Yellow
Write-Host "3. Name it 'MinuteMate Integration'" -ForegroundColor Yellow
Write-Host "4. Copy the Internal Integration Token (starts with secret_)" -ForegroundColor Yellow
Write-Host "5. Create a page in Notion and copy its ID from the URL" -ForegroundColor Yellow
Write-Host "6. Share the page with your integration" -ForegroundColor Yellow
Write-Host ""
Write-Host "After completing the steps above, enter your details below:" -ForegroundColor White
Write-Host ""

$NOTION_TOKEN = Read-Host "Enter your Notion Integration Token"
$NOTION_PAGE_ID = Read-Host "Enter your Notion Page ID"

Write-Host ""
Write-Host "Updating server/.env file..." -ForegroundColor Yellow

$serverEnvContent = @"
# Server Configuration
NODE_ENV=development
PORT=5000

# Google OAuth Configuration (optional)
GOOGLE_CLIENT_ID=your-google-client-id-here
GOOGLE_CLIENT_SECRET=your-google-client-secret-here
FRONTEND_URL=http://localhost:3001

# Notion Configuration
NOTION_TOKEN=$NOTION_TOKEN
NOTION_PARENT_PAGE_ID=$NOTION_PAGE_ID

# Whisper API Configuration
WHISPER_API_URL=http://localhost:5001
"@

$serverEnvContent | Out-File -FilePath "server\.env" -Encoding UTF8

Write-Host ""
Write-Host "✅ Notion configuration updated!" -ForegroundColor Green
Write-Host ""
Write-Host "Your Notion integration is now configured." -ForegroundColor White
Write-Host "Restart your services to apply the changes." -ForegroundColor White
Write-Host ""
Read-Host "Press Enter to continue" 