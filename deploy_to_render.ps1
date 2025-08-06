# Deploy to Render Script
Write-Host "🚀 Deploying Minute Mate to Render..." -ForegroundColor Green

# Check if git is initialized
if (-not (Test-Path ".git")) {
    Write-Host "❌ Git repository not found. Please initialize git first:" -ForegroundColor Red
    Write-Host "   git init" -ForegroundColor Yellow
    Write-Host "   git add ." -ForegroundColor Yellow
    Write-Host "   git commit -m 'Initial commit'" -ForegroundColor Yellow
    exit 1
}

# Check if changes are committed
$status = git status --porcelain
if ($status) {
    Write-Host "⚠️  You have uncommitted changes. Please commit them first:" -ForegroundColor Yellow
    Write-Host "   git add ." -ForegroundColor Yellow
    Write-Host "   git commit -m 'Prepare for deployment'" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Repository is ready for deployment" -ForegroundColor Green

Write-Host "📋 Next steps:" -ForegroundColor Cyan
Write-Host "1. Go to https://dashboard.render.com/" -ForegroundColor White
Write-Host "2. Click 'New +' → 'Blueprint'" -ForegroundColor White
Write-Host "3. Connect your GitHub repository" -ForegroundColor White
Write-Host "4. Render will automatically detect the render.yaml file" -ForegroundColor White
Write-Host "5. Set the following environment variables:" -ForegroundColor White
Write-Host "   - GOOGLE_CLIENT_ID: Your Google OAuth client ID" -ForegroundColor Yellow
Write-Host "   - GOOGLE_CLIENT_SECRET: Your Google OAuth client secret" -ForegroundColor Yellow
Write-Host "   - NOTION_TOKEN: Your Notion integration token (optional)" -ForegroundColor Yellow
Write-Host "   - NOTION_PARENT_PAGE_ID: Your Notion page ID (optional)" -ForegroundColor Yellow
Write-Host "   - FRONTEND_URL: Your Vercel frontend URL (set after Vercel deployment)" -ForegroundColor Yellow
Write-Host "6. Click Apply to deploy" -ForegroundColor White

Write-Host "🌐 After deployment, update your Vercel environment variables:" -ForegroundColor Cyan
Write-Host "   - REACT_APP_API_BASE_URL: https://your-backend-service-name.onrender.com" -ForegroundColor Yellow
Write-Host "   - REACT_APP_WHISPER_API_URL: https://your-whisper-service-name.onrender.com" -ForegroundColor Yellow

Write-Host "📚 For detailed instructions, see DEPLOYMENT_GUIDE.md" -ForegroundColor Cyan 