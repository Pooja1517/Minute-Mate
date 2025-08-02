# Test Production Setup Script
Write-Host "🧪 Testing Production Setup..." -ForegroundColor Green

Write-Host ""
Write-Host "🔗 Testing Backend Service..." -ForegroundColor Yellow
try {
    $backendResponse = Invoke-WebRequest -Uri "https://minute-mate-backend.onrender.com/health" -TimeoutSec 10
    Write-Host "✅ Backend is accessible: $($backendResponse.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "❌ Backend not accessible yet. Make sure it's deployed to Render." -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Gray
}

Write-Host ""
Write-Host "🔗 Testing Whisper Service..." -ForegroundColor Yellow
try {
    $whisperResponse = Invoke-WebRequest -Uri "https://minute-mate-whisper.onrender.com/health" -TimeoutSec 10
    Write-Host "✅ Whisper API is accessible: $($whisperResponse.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "❌ Whisper API not accessible yet. Make sure it's deployed to Render." -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Gray
}

Write-Host ""
Write-Host "📋 Current Configuration:" -ForegroundColor Cyan
Write-Host "   Backend URL: https://minute-mate-backend.onrender.com" -ForegroundColor White
Write-Host "   Whisper URL: https://minute-mate-whisper.onrender.com" -ForegroundColor White

Write-Host ""
Write-Host "🎯 Next Steps:" -ForegroundColor Cyan
Write-Host "1. Deploy backend services to Render using the names above" -ForegroundColor White
Write-Host "2. Deploy frontend to Vercel" -ForegroundColor White
Write-Host "3. Test with local backend stopped" -ForegroundColor White

Write-Host ""
Write-Host "📖 See PRODUCTION_SETUP.md for detailed deployment instructions" -ForegroundColor Yellow 