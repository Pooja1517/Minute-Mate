# Deployment Script for Minute Mate
Write-Host "🚀 Preparing Minute Mate for Deployment..." -ForegroundColor Green

# Check if git is initialized
if (-not (Test-Path ".git")) {
    Write-Host "❌ Git repository not found. Please initialize git first." -ForegroundColor Red
    exit 1
}

# Add all changes
Write-Host "📁 Adding files to git..." -ForegroundColor Yellow
git add .

# Check if there are changes to commit
$status = git status --porcelain
if (-not $status) {
    Write-Host "✅ No changes to commit. Repository is up to date." -ForegroundColor Green
} else {
    # Commit changes
    Write-Host "💾 Committing changes..." -ForegroundColor Yellow
    git commit -m "Prepare for deployment - Add deployment configs and environment variables"
    
    # Push to GitHub
    Write-Host "📤 Pushing to GitHub..." -ForegroundColor Yellow
    git push origin main
    
    Write-Host "✅ Changes pushed to GitHub successfully!" -ForegroundColor Green
}

Write-Host ""
Write-Host "🎯 Next Steps for Deployment:" -ForegroundColor Cyan
Write-Host "1. Deploy backend services to Render:" -ForegroundColor White
Write-Host "   - Go to https://dashboard.render.com/" -ForegroundColor Gray
Write-Host "   - Create two web services (Node.js + Python)" -ForegroundColor Gray
Write-Host "   - Use the render.yaml configuration" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Deploy frontend to Vercel:" -ForegroundColor White
Write-Host "   - Go to https://vercel.com/dashboard" -ForegroundColor Gray
Write-Host "   - Import your GitHub repository" -ForegroundColor Gray
Write-Host "   - Set root directory to 'client'" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Configure environment variables:" -ForegroundColor White
Write-Host "   - Set API URLs in Vercel" -ForegroundColor Gray
Write-Host "   - Set OAuth credentials in Render" -ForegroundColor Gray
Write-Host "   - Update Google OAuth redirect URIs" -ForegroundColor Gray
Write-Host ""
Write-Host "📖 See DEPLOYMENT_GUIDE.md for detailed instructions" -ForegroundColor Yellow
Write-Host ""
Write-Host "🔗 Your Whisper API is ready for large projects with:" -ForegroundColor Green
Write-Host "   ✅ 10MB file size limit" -ForegroundColor Gray
Write-Host "   ✅ Optimized settings for large files" -ForegroundColor Gray
Write-Host "   ✅ Memory management and cleanup" -ForegroundColor Gray
Write-Host "   ✅ Fallback mechanisms" -ForegroundColor Gray
Write-Host ""
Write-Host "🎉 Ready to deploy!" -ForegroundColor Green 