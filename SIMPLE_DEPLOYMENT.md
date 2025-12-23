# 🚀 Domain File Generator - Simple Deployment Guide

**For Non-Technical Users**

This guide will help you deploy the Domain File Generator to a server so your entire team can use it through their web browsers.

---

## 📋 What You'll Need

1. **A server or computer** that stays on 24/7 (can be Windows or Linux)
2. **30 minutes of time**
3. **This guide** (that's it!)

---

## 🎯 End Result

After following these steps:
- Your team visits: `http://192.168.1.XXX:5000` (your server address)
- They see the Domain File Generator
- They can use it without installing anything
- Works on any device with a web browser

---

# 🪟 Windows Server Deployment (Easiest)

## Step 1: Check if Python is Installed

1. Press `Windows Key + R`
2. Type: `cmd`
3. Press Enter
4. In the black window, type: `python --version`
5. Press Enter

**Do you see something like "Python 3.10.X"?**
- ✅ **YES** → Go to Step 3
- ❌ **NO** → Continue to Step 2

---

## Step 2: Install Python (One-Time Setup)

1. **Download Python:**
   - Open your web browser
   - Go to: https://www.python.org/downloads/
   - Click the big yellow **"Download Python"** button
   - Save the file

2. **Install Python:**
   - Double-click the downloaded file
   - ⚠️ **IMPORTANT:** Check the box that says **"Add Python to PATH"**
   - Click **"Install Now"**
   - Wait for it to finish (2-3 minutes)
   - Click **"Close"**

3. **Verify it worked:**
   - Press `Windows Key + R`
   - Type: `cmd`
   - Press Enter
   - Type: `python --version`
   - You should see "Python 3.X.X"

---

## Step 3: Copy the Application to Your Server

1. **Copy the entire folder:**
   - Find the `domain-generator` folder on your computer
   - Current location: `C:\Users\BurhanuddinBhori\.gemini\antigravity\playground\ethereal-chromosphere\domain-generator`

2. **Copy it to a simple location on the server:**
   - Recommended: `C:\DomainGenerator\`
   - Just copy and paste the whole folder

---

## Step 4: Install Required Libraries

1. **Open Command Prompt:**
   - Press `Windows Key + R`
   - Type: `cmd`
   - Press Enter

2. **Go to the application folder:**
   ```
   cd C:\DomainGenerator
   ```
   Press Enter

3. **Install the libraries:**
   ```
   pip install -r requirements.txt
   ```
   Press Enter
   
   Wait 1-2 minutes while it downloads and installs everything.
   
   You'll see lots of text - that's normal!
   
   When you see your folder path again (`C:\DomainGenerator>`), it's done.

---

## Step 5: Make It Accessible to Others

1. **Open the app.py file:**
   - Right-click on `app.py` in the folder
   - Click **"Edit with Notepad"**

2. **Find the last line:**
   - Scroll to the very bottom
   - You'll see: `app.run(debug=True, port=5000)`

3. **Change it to:**
   ```python
   app.run(debug=False, host='0.0.0.0', port=5000)
   ```
   
   Copy and paste this exactly!

4. **Save and close:**
   - Click **File → Save**
   - Close Notepad

---

## Step 6: Allow Through Firewall

1. **Open Windows Defender Firewall:**
   - Press `Windows Key`
   - Type: `firewall`
   - Click **"Windows Defender Firewall with Advanced Security"**

2. **Create a new rule:**
   - Click **"Inbound Rules"** on the left
   - Click **"New Rule..."** on the right
   - Select **"Port"** → Click **Next**
   - Keep **"TCP"** selected
   - In "Specific local ports", type: `5000`
   - Click **Next**
   - Select **"Allow the connection"**
   - Click **Next**
   - Check all three boxes (Domain, Private, Public)
   - Click **Next**
   - Name: **"Domain Generator"**
   - Click **Finish**

---

## Step 7: Find Your Server's IP Address

1. **Open Command Prompt:**
   - Press `Windows Key + R`
   - Type: `cmd`
   - Press Enter

2. **Get the IP address:**
   ```
   ipconfig
   ```
   Press Enter

3. **Look for "IPv4 Address":**
   - You'll see something like: `192.168.1.100`
   - **Write this down!** This is your server address.

---

## Step 8: Start the Application

1. **Open Command Prompt:**
   - Press `Windows Key + R`
   - Type: `cmd`
   - Press Enter

2. **Go to the application folder:**
   ```
   cd C:\DomainGenerator
   ```

3. **Start the application:**
   ```
   python app.py
   ```
   
   You'll see:
   ```
   🚀 Domain File Generator - Madison Logic
   Server starting at: http://localhost:5000
   ```
   
   **Don't close this window!** The application is running.

---

## Step 9: Test It!

1. **On the server computer:**
   - Open any web browser
   - Go to: `http://localhost:5000`
   - You should see the Domain File Generator!

2. **On another computer (in the same network):**
   - Open any web browser
   - Go to: `http://192.168.1.XXX:5000` (use the IP you wrote down in Step 7)
   - You should see the Domain File Generator!

**🎉 IT WORKS!** Share this address with your team!

---

## Step 10: Make It Run Automatically (Optional but Recommended)

So you don't have to manually start it every time:

### Method 1: Simple Batch File

1. **Create a new file:**
   - Right-click in `C:\DomainGenerator`
   - **New → Text Document**
   - Name it: `start.bat` (not start.bat.txt!)

2. **Edit the file:**
   - Right-click → **Edit**
   - Paste this:
   ```batch
   @echo off
   cd C:\DomainGenerator
   python app.py
   pause
   ```
   - Save and close

3. **To start the app:**
   - Just double-click `start.bat`

### Method 2: Auto-Start on Boot (Advanced)

1. **Download NSSM:**
   - Go to: https://nssm.cc/download
   - Download the latest version
   - Extract the ZIP file

2. **Open Command Prompt as Administrator:**
   - Press `Windows Key`
   - Type: `cmd`
   - Right-click **"Command Prompt"**
   - Click **"Run as administrator"**

3. **Go to NSSM folder:**
   ```
   cd C:\path\to\nssm\win64
   ```

4. **Install as service:**
   ```
   nssm install DomainGenerator
   ```

5. **A window will open:**
   - **Path:** Click **"..."** and find `python.exe` (usually `C:\Python310\python.exe`)
   - **Startup directory:** `C:\DomainGenerator`
   - **Arguments:** `app.py`
   - Click **"Install service"**

6. **Start the service:**
   ```
   nssm start DomainGenerator
   ```

Now it will auto-start when the server boots!

---

## 🆘 Troubleshooting

### "Port 5000 is already in use"

**Solution:** Change the port number
1. Edit `app.py`
2. Change `port=5000` to `port=5001`
3. Update firewall rule for port 5001
4. Tell users to use: `http://server:5001`

### "Can't access from other computers"

**Checklist:**
- ✅ Did you change `app.py` to use `host='0.0.0.0'`?
- ✅ Did you add the firewall rule?
- ✅ Is the Command Prompt window still open and running?
- ✅ Are both computers on the same network?

### "Python not found"

**Solution:**
1. Reinstall Python
2. Make sure to check **"Add Python to PATH"**

---

## 📧 Share This With Your Team

Copy and send this message to your team:

---

**Subject: New Domain File Generator Tool Available!**

Hi Team,

We now have a web-based Domain File Generator available!

**To use it:**
1. Open your web browser (Chrome, Firefox, Edge, Safari)
2. Go to: `http://192.168.1.XXX:5000` (replace with your server IP)
3. Follow the instructions on the page

**You don't need to install anything!** Just use your browser.

**How to use:**
1. Download the sample template
2. Fill in your data (TAL names, countries, and domain mappings)
3. Upload your file
4. Download the results

Questions? Contact IT Support.

---

## ✅ Summary

**What you did:**
1. ✅ Installed Python on the server (one time)
2. ✅ Copied the application folder
3. ✅ Installed required libraries
4. ✅ Configured firewall
5. ✅ Started the application

**What your team needs:**
- ✅ Just a web browser
- ✅ The server IP address
- ✅ Nothing else!

**Maintenance:**
- Just keep the server running
- Restart the application if you reboot the server (or use NSSM for auto-start)

---

## 🎓 Need More Help?

If you get stuck:
1. Check the Troubleshooting section above
2. Contact your IT department
3. Make sure the Command Prompt window is still open and showing the server messages

---

**Congratulations! You've deployed a web application! 🎉**
