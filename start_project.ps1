# MinuteMate Project Startup Script
Write-Host "🚀 Starting MinuteMate Project..." -ForegroundColor Green

# Kill any existing processes
Write-Host "Stopping existing processes..." -ForegroundColor Yellow
Get-Process python, node -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

# Start Python Whisper API
Write-Host "Starting Python Whisper API..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'C:\Users\T1IN\minute-mate'; python whisper_api.py" -WindowStyle Normal

# Wait for Python to start
Start-Sleep -Seconds 10

# Start Node.js Server
Write-Host "Starting Node.js Server..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'C:\Users\T1IN\minute-mate\server'; node index.js" -WindowStyle Normal

# Wait for Node.js to start
Start-Sleep -Seconds 5

# Start React Frontend
Write-Host "Starting React Frontend..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'C:\Users\T1IN\minute-mate\client'; npm start" -WindowStyle Normal

Write-Host "✅ All services started!" -ForegroundColor Green
Write-Host "📱 Frontend: http://localhost:3000" -ForegroundColor White
Write-Host "🔧 Backend: http://localhost:5000" -ForegroundColor White
Write-Host "🤖 Whisper API: http://localhost:5001" -ForegroundColor White
Write-Host ""
Write-Host "Keep all terminal windows open while using the application!" -ForegroundColor Yellow 