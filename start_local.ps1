# Start Local Development Environment
Write-Host "🚀 Starting Minute Mate Local Development..." -ForegroundColor Green

# Check if Node.js is installed
try {
    $nodeVersion = node --version
    Write-Host "✅ Node.js found: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js not found. Please install Node.js first." -ForegroundColor Red
    exit 1
}

# Check if Python is installed
try {
    $pythonVersion = python --version
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python first." -ForegroundColor Red
    exit 1
}

Write-Host "📋 Starting services..." -ForegroundColor Cyan
Write-Host "1. Backend (Node.js) - Port 5000" -ForegroundColor White
Write-Host "2. Whisper API (Python) - Port 5001" -ForegroundColor White
Write-Host "3. Frontend (React) - Port 3000" -ForegroundColor White

Write-Host "`n🔧 Manual startup commands:" -ForegroundColor Yellow
Write-Host "Terminal 1 (Backend):" -ForegroundColor White
Write-Host "  cd server && npm install && node index.js" -ForegroundColor Gray

Write-Host "`nTerminal 2 (Whisper API):" -ForegroundColor White
Write-Host "  python -m pip install -r requirements.txt && python whisper_api.py" -ForegroundColor Gray

Write-Host "`nTerminal 3 (Frontend):" -ForegroundColor White
Write-Host "  cd client && npm install && npm start" -ForegroundColor Gray

Write-Host "`n🌐 After starting all services:" -ForegroundColor Cyan
Write-Host "  - Frontend: http://localhost:3000" -ForegroundColor White
Write-Host "  - Backend: http://localhost:5000/health" -ForegroundColor White
Write-Host "  - Whisper API: http://localhost:5001/health" -ForegroundColor White

Write-Host "`n💡 Tip: Open multiple terminal windows/tabs to run each service" -ForegroundColor Yellow 