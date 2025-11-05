@echo off
color 0A
echo.
echo  ██████╗ ███████╗██████╗ ███████╗██╗██████╗ ███████╗██████╗  ██████╗ ████████╗
echo  ██╔══██╗██╔════╝██╔══██╗██╔════╝██║██╔══██╗██╔════╝██╔══██╗██╔═══██╗╚══██╔══╝
echo  ██████╔╝█████╗  ██║  ██║███████╗██║██║  ██║█████╗  ██████╔╝██║   ██║   ██║   
echo  ██╔══██╗██╔══╝  ██║  ██║╚════██║██║██║  ██║██╔══╝  ██╔══██╗██║   ██║   ██║   
echo  ██████╔╝███████╗██████╔╝███████║██║██████╔╝███████╗██████╔╝╚██████╔╝   ██║   
echo  ╚═════╝ ╚══════╝╚═════╝ ╚══════╝╚═╝╚═════╝ ╚══════╝╚═════╝  ╚═════╝    ╚═╝   
echo.
echo                           🏥 QUICK DEPLOYMENT SCRIPT 🏥
echo.
echo ================================================================================
echo                        DEPLOY YOUR APP IN 3 SIMPLE STEPS!
echo ================================================================================
echo.

echo 📋 STEP 1: Create GitHub Repository
echo ────────────────────────────────────
echo 1. Go to https://github.com
echo 2. Click "New Repository" 
echo 3. Name it: bedsidebot-app
echo 4. Make it PUBLIC
echo 5. Click "Create Repository"
echo.
pause

echo.
echo 📤 STEP 2: Push Your Code to GitHub
echo ──────────────────────────────────────
set /p username="Enter your GitHub username: "

echo.
echo Pushing to GitHub...
git remote remove origin 2>nul
git remote add origin https://github.com/%username%/bedsidebot-app.git
git branch -M main
git push -u origin main

if %errorlevel% equ 0 (
    echo ✅ SUCCESS! Code pushed to GitHub!
) else (
    echo ❌ Error pushing to GitHub. Make sure you created the repository first.
    pause
    exit /b 1
)

echo.
echo 🚀 STEP 3: Deploy on Railway
echo ────────────────────────────
echo 1. Go to https://railway.app
echo 2. Sign up with your GitHub account
echo 3. Click "New Project"
echo 4. Select "Deploy from GitHub repo"
echo 5. Choose "bedsidebot-app"
echo 6. Wait 2-3 minutes for deployment
echo.

echo ================================================================================
echo                              🎉 DEPLOYMENT COMPLETE! 🎉
echo ================================================================================
echo.
echo Your BedsideBot will be available at:
echo 🌐 https://bedsidebot-app-production.up.railway.app
echo.
echo You can now access your app from ANY computer with internet!
echo Share this URL with your team to use BedsideBot on multiple PCs.
echo.
echo 📖 For detailed instructions, check DEPLOYMENT_GUIDE.md
echo.
pause