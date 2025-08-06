# Setup Local Environment Variables
Write-Host "🔧 Setting up local environment variables..." -ForegroundColor Green

$envFile = "client\.env.local"

# Check if file already exists
if (Test-Path $envFile) {
    Write-Host "⚠️  .env.local already exists. Backing up..." -ForegroundColor Yellow
    Copy-Item $envFile "$envFile.backup"
}

# Create the environment file
$envContent = @"
# Local Development Environment Variables
# This file is used when running locally (npm start)

# Backend API URL (local)
REACT_APP_API_BASE_URL=http://localhost:5000

# Whisper API URL (local)
REACT_APP_WHISPER_API_URL=http://localhost:5001
"@

# Write the content to file
$envContent | Out-File -FilePath $envFile -Encoding UTF8

Write-Host "✅ Created $envFile" -ForegroundColor Green
Write-Host "📋 File contents:" -ForegroundColor Cyan
Get-Content $envFile | ForEach-Object { Write-Host "   $_" -ForegroundColor Gray }

Write-Host "`n🚀 Next steps:" -ForegroundColor Cyan
Write-Host "1. Start your local services:" -ForegroundColor White
Write-Host "   Terminal 1: cd server && npm install && node index.js" -ForegroundColor Gray
Write-Host "   Terminal 2: python -m pip install -r requirements.txt && python whisper_api.py" -ForegroundColor Gray
Write-Host "   Terminal 3: cd client && npm install && npm start" -ForegroundColor Gray

Write-Host "`n2. For Vercel deployment:" -ForegroundColor White
Write-Host "   - Deploy backend to Render" -ForegroundColor Gray
Write-Host "   - Set environment variables in Vercel dashboard" -ForegroundColor Gray
Write-Host "   - See ENVIRONMENT_SETUP.md for details" -ForegroundColor Gray

Write-Host "`n💡 The app will now automatically use localhost URLs when running locally!" -ForegroundColor Green 