@echo off
echo ========================================
echo BedsideBot GitHub Deployment Helper
echo ========================================
echo.

echo Step 1: Make sure you created a GitHub repository named 'bedsidebot-app'
echo Step 2: Replace YOUR_USERNAME with your actual GitHub username below
echo.

set /p username="Enter your GitHub username: "
echo.

echo Adding GitHub remote...
git remote remove origin 2>nul
git remote add origin https://github.com/%username%/bedsidebot-app.git

echo.
echo Pushing to GitHub...
git branch -M main
git push -u origin main

echo.
echo ========================================
echo SUCCESS! Your code is now on GitHub!
echo ========================================
echo.
echo Next steps:
echo 1. Go to Railway.app
echo 2. Sign up with GitHub
echo 3. Deploy from your bedsidebot-app repository
echo 4. Your app will be live in minutes!
echo.
pause