@echo off
REM 🚀 Render Deployment Helper Script for Minute Mate (Windows)
echo 🚀 Starting Render deployment process...

REM Check if git is available
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git is not installed. Please install git first.
    pause
    exit /b 1
)

REM Check if we're in a git repository
if not exist ".git" (
    echo ❌ Not in a git repository. Please run this from your project root.
    pause
    exit /b 1
)

REM Check current git status
echo 📋 Checking git status...
git status --porcelain

REM Ask user if they want to commit changes
set /p commit_choice="🤔 Do you want to commit and push your changes? (y/n): "
if /i "%commit_choice%"=="y" (
    echo 📝 Committing changes...
    
    REM Add all files
    git add .
    
    REM Commit with timestamp
    for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
    set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
    set "HH=%dt:~8,2%" & set "Min=%dt:~10,2%" & set "Sec=%dt:~12,2%"
    set "datestamp=%YYYY%-%MM%-%DD% %HH%:%Min%:%Sec%"
    
    git commit -m "🚀 Render deployment optimization - %datestamp%"
    
    REM Push to remote
    echo 🚀 Pushing to remote repository...
    git push
    
    echo ✅ Code pushed successfully!
) else (
    echo ⏭️  Skipping git operations...
)

echo.
echo 🎯 Next Steps for Render Deployment:
echo.
echo 1. 📱 Go to https://render.com and sign in
echo 2. 🔗 Connect your GitHub repository
echo 3. 📋 Create a new Blueprint
echo 4. 📁 Use the file: render-optimized.yaml
echo 5. ⚙️  Set environment variables:
echo    - NOTION_TOKEN
echo    - NOTION_DATABASE_ID
echo    - GOOGLE_CLIENT_ID
echo    - GOOGLE_CLIENT_SECRET
echo    - FRONTEND_URL
echo.
echo 6. 🚀 Deploy and wait for services to start
echo 7. 🧪 Test with health checks:
echo    - Frontend: /
echo    - Backend: /health
echo    - Whisper: /health
echo.
echo 📚 For detailed instructions, see: RENDER_DEPLOYMENT_FIX.md
echo 🔧 For quick testing, see: ngrok-quick-test.md
echo.
echo 🎉 Good luck with your deployment!
pause
