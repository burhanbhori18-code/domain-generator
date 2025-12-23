@echo off
echo ===================================================
echo 🚀 Deploying to NEW GitHub Repository
echo ===================================================

:: 1. Clean up old git configuration if it exists
if exist .git (
    echo Cleaning up old git folder...
    rmdir /s /q .git
)

:: 2. Initialize new repository
echo Initializing git...
git init

:: 3. Add all files
echo Adding files...
git add .

:: 4. Commit changes
echo Committing changes...
git commit -m "Full update: Campaign enhancement and partial processing logic"

:: 5. Rename branch to main
git branch -M main

:: 6. Add new remote origin
echo Adding remote origin...
git remote add origin https://github.com/burhanbhori18-code/domain-generator.git

:: 7. Push to GitHub
echo Pushing code to GitHub...
git push -u origin main --force

echo.
echo ===================================================
echo ✅ Done! Your code is pushed to the new repository.
echo Render will now detect the changes and redeploy automatically.
echo ===================================================
pause
