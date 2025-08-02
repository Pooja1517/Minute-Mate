Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    MinuteMate - Starting All Services" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "1. Killing any existing processes..." -ForegroundColor Yellow
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
Get-Process node -ErrorAction SilentlyContinue | Stop-Process -Force

Write-Host "2. Starting Whisper API (Real) on port 5001..." -ForegroundColor Green
Start-Process -WindowStyle Normal python -ArgumentList "whisper_api.py"

Write-Host "3. Starting Node.js Server on port 5000..." -ForegroundColor Green
Start-Process -WindowStyle Normal node -ArgumentList "index.js" -WorkingDirectory "server"

Write-Host "4. Starting React Frontend on port 3001..." -ForegroundColor Green
Start-Process -WindowStyle Normal npm -ArgumentList "start" -WorkingDirectory "client"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    All Services Started!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Please wait 30-60 seconds for all services to start." -ForegroundColor White
Write-Host ""
Write-Host "Then open your browser and go to:" -ForegroundColor White
Write-Host "    http://localhost:3001" -ForegroundColor Green
Write-Host ""
Write-Host "Service Status:" -ForegroundColor White
Write-Host "- Whisper API: http://localhost:5001/health" -ForegroundColor Gray
Write-Host "- Node.js Server: http://localhost:5000/health" -ForegroundColor Gray
Write-Host "- React Frontend: http://localhost:3001" -ForegroundColor Gray
Write-Host ""
Write-Host "Note: You should see 3 new terminal windows open." -ForegroundColor Yellow
Write-Host "Keep them all running while using the application." -ForegroundColor Yellow
Write-Host ""
Read-Host "Press Enter to continue" 