@echo off
echo Stopping Node.js server...
taskkill /f /im node.exe 2>nul
timeout /t 2 /nobreak >nul
echo Starting Node.js server...
cd server
node index.js 