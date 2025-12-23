@echo off
echo ===================================================
echo 🚀 Updating GitHub Repository
echo ===================================================

:: 1. Add only changed files
echo Adding changed files...
git add .

:: 2. Commit changes
echo Committing changes...
git commit -m "Performance optimization: Caching and Timeout Fixes"

:: 3. Push to GitHub
echo Pushing code to GitHub...
git push origin main

echo.
echo ===================================================
echo ✅ Done! Changes pushed.
echo Render should redeploy automatically in a few minutes.
echo ===================================================
pause
