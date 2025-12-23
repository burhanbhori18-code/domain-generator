# 🚀 Deploy Commands - Copy and Paste These!

**IMPORTANT: After installing Git, you need to close and reopen Command Prompt!**

Follow these steps:

---

## Step 1: Close Current Terminal

If you have any Command Prompt or PowerShell windows open:
- Close them all
- This is necessary for Git to be recognized

---

## Step 2: Open New Command Prompt

1. Press `Windows Key + R`
2. Type: `cmd`
3. Press Enter

---

## Step 3: Navigate to Your Project Folder

Copy and paste this command:

```bash
cd C:\Users\BurhanuddinBhori\.gemini\antigravity\playground\ethereal-chromosphere\domain-generator
```

Press Enter.

---

## Step 4: Verify Git is Working

Copy and paste this command:

```bash
git --version
```

Press Enter.

You should see something like: `git version 2.x.x`

If you see an error, Git isn't installed correctly. Try reinstalling from: https://git-scm.com/download/win

---

## Step 5: Configure Git (One-Time Setup)

Copy and paste these commands ONE AT A TIME:

**Command 1 - Set your email:**
```bash
git config --global user.email "burhanbhori18@gmail.com"
```

**Command 2 - Set your name:**
```bash
git config --global user.name "Burhan Bhori"
```

---

## Step 6: Initialize Git Repository

Copy and paste these commands ONE AT A TIME:

**Command 1 - Initialize Git:**
```bash
git init
```

**Command 2 - Add all files:**
```bash
git add .
```

**Command 3 - Commit files:**
```bash
git commit -m "Initial commit - Domain File Generator"
```

---

## Step 7: Create GitHub Repository

Now we need to create a repository on GitHub:

1. **Open your web browser**
2. **Go to:** https://github.com/new
3. **Log in** if asked (use: burhanbhori18@gmail.com)
   - If you don't have an account, click "Sign up" and create one first
4. **Fill in the form:**
   - Repository name: `domain-generator`
   - Description: "Web-based domain file generator with Madison Logic branding"
   - Keep it: **Public**
   - **DO NOT** check "Add a README file"
   - **DO NOT** check "Add .gitignore"
   - **DO NOT** choose a license
5. **Click:** "Create repository"

---

## Step 8: Connect to GitHub

After creating the repository, GitHub will show you some commands.

**Copy and paste these commands** (replace YOUR-USERNAME with your actual GitHub username):

**Command 1 - Add remote:**
```bash
git remote add origin https://github.com/YOUR-USERNAME/domain-generator.git
```

**Command 2 - Rename branch:**
```bash
git branch -M main
```

**Command 3 - Push to GitHub:**
```bash
git push -u origin main
```

When asked for credentials:
- **Username:** Your GitHub username
- **Password:** Use a **Personal Access Token** (NOT your password)

---

## Step 9: Create GitHub Personal Access Token

If you don't have a token yet:

1. **Go to:** https://github.com/settings/tokens
2. **Click:** "Generate new token" → "Generate new token (classic)"
3. **Give it a name:** "Render Deploy"
4. **Select scopes:** Check the box for **repo** (this checks all sub-boxes automatically)
5. **Click:** "Generate token" at the bottom
6. **COPY THE TOKEN!** You won't see it again!
7. **Use this token as your password** when Git asks

---

## Step 10: Deploy to Render

Once your code is on GitHub:

1. **Go to:** https://render.com
2. **Sign up** or **Log in**
   - Easiest: Click "Sign In with GitHub"
3. **From dashboard, click:** "New +" button
4. **Select:** "Web Service"
5. **Connect your repository:**
   - Find: `domain-generator`
   - Click: "Connect"
6. **Configure:**
   - Name: `domain-generator` (or any name you want)
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Instance Type: **Free**
7. **Click:** "Create Web Service"
8. **Wait 3-5 minutes** for deployment
9. **Your URL will be:** `https://domain-generator-XXXXX.onrender.com`

---

## ✅ Summary

**Commands you need to run** (in order):

1. Close and reopen Command Prompt
2. `cd C:\Users\BurhanuddinBhori\.gemini\antigravity\playground\ethereal-chromosphere\domain-generator`
3. `git --version` (verify it works)
4. `git config --global user.email "burhanbhori18@gmail.com"`
5. `git config --global user.name "Burhan Bhori"`
6. `git init`
7. `git add .`
8. `git commit -m "Initial commit - Domain File Generator"`
9. Create GitHub repository (in browser)
10. `git remote add origin https://github.com/YOUR-USERNAME/domain-generator.git`
11. `git branch -M main`
12. `git push -u origin main`
13. Deploy on Render (in browser)

**Total time: 10-15 minutes**

---

## 🆘 If You Get Stuck

**Git not recognized:**
- Reinstall Git from: https://git-scm.com/download/win
- Make sure to close and reopen Command Prompt

**Git push asks for password:**
- Use your GitHub Personal Access Token, NOT your password
- Create token at: https://github.com/settings/tokens

**Render deployment fails:**
- Check the logs in Render dashboard
- Make sure all files were pushed to GitHub
- Verify `render.yaml` and `requirements.txt` are present

---

**Once you complete these steps, your app will be live! 🎉**

**Your team will access it at:** `https://your-app-name.onrender.com`
