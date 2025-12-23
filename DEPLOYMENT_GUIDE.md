# Server Deployment Guide

## 🎯 Overview

This guide explains how to deploy the Domain File Generator on a **shared server** so multiple users can access it via web browser **without installing anything** on their computers.

---

## ✅ What Users Need

When deployed to a server, users only need:
- ✅ **Web browser** (Chrome, Firefox, Edge, Safari)
- ✅ **Network access** to the server
- ❌ **NO Python installation required**
- ❌ **NO software installation required**
- ❌ **NO technical knowledge required**

Users will simply visit: `http://[your-server-ip]:5000` or `http://yourdomain.com`

---

## 🖥️ Server Requirements

### Hardware
- **CPU:** Any modern CPU (2+ cores recommended)
- **RAM:** 2GB minimum, 4GB recommended
- **Storage:** 10GB free space
- **Network:** Stable internet/LAN connection

### Software
- **Operating System:** Windows Server 2016+ or Linux (Ubuntu 20.04+, CentOS 7+)
- **Python:** 3.7 or higher
- **Web browser** (for testing)

---

## 📦 Deployment Options

### **Option 1: Quick Internal Deployment** (Recommended for testing)

Perfect for small teams on a local network.

#### Windows Server:

1. **Copy the folder** to your server:
   ```
   C:\inetpub\domain-generator\
   ```

2. **Install Python** on the server (one-time setup):
   - Download from: https://www.python.org/downloads/
   - Check "Add Python to PATH" during installation

3. **Open Command Prompt** on the server and navigate to the folder:
   ```cmd
   cd C:\inetpub\domain-generator
   ```

4. **Install dependencies** (one-time setup):
   ```cmd
   pip install -r requirements.txt
   ```

5. **Edit app.py** - Change the last line to:
   ```python
   app.run(debug=False, host='0.0.0.0', port=5000)
   ```

6. **Run the application**:
   ```cmd
   python app.py
   ```

7. **Configure Windows Firewall**:
   - Open Windows Defender Firewall
   - Click "Advanced settings"
   - Click "Inbound Rules" → "New Rule"
   - Select "Port" → "TCP" → Enter "5000"
   - Allow the connection → Name it "Domain Generator"

8. **Find your server IP**:
   ```cmd
   ipconfig
   ```
   Look for "IPv4 Address" (e.g., 192.168.1.100)

9. **Users access via**:
   ```
   http://192.168.1.100:5000
   ```

#### Linux Server (Ubuntu/CentOS):

```bash
# 1. Copy folder to server
cd /var/www/domain-generator

# 2. Install Python and pip
sudo apt update
sudo apt install python3 python3-pip

# 3. Install dependencies
pip3 install -r requirements.txt

# 4. Edit app.py (change last line)
# app.run(debug=False, host='0.0.0.0', port=5000)

# 5. Run the application
python3 app.py

# 6. Configure firewall
sudo ufw allow 5000/tcp
```

---

### **Option 2: Production Deployment with Auto-Start**

For 24/7 availability and automatic restart.

#### Windows (Using NSSM - Non-Sucking Service Manager):

1. **Download NSSM**: https://nssm.cc/download
   
2. **Install as Windows Service**:
   ```cmd
   nssm install DomainGenerator "C:\Python310\python.exe" "C:\inetpub\domain-generator\app.py"
   nssm set DomainGenerator AppDirectory "C:\inetpub\domain-generator"
   nssm start DomainGenerator
   ```

3. **Service will auto-start** on server reboot

#### Linux (Using systemd):

1. **Create service file**:
   ```bash
   sudo nano /etc/systemd/system/domain-generator.service
   ```

2. **Add this content**:
   ```ini
   [Unit]
   Description=Domain File Generator
   After=network.target

   [Service]
   Type=simple
   User=www-data
   WorkingDirectory=/var/www/domain-generator
   ExecStart=/usr/bin/python3 /var/www/domain-generator/app.py
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

3. **Enable and start**:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable domain-generator
   sudo systemctl start domain-generator
   ```

---

### **Option 3: Professional Production Setup**

For large organizations with high traffic.

#### Using Gunicorn + Nginx (Linux):

1. **Install Gunicorn**:
   ```bash
   pip3 install gunicorn
   ```

2. **Run with Gunicorn**:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   ```

3. **Install Nginx**:
   ```bash
   sudo apt install nginx
   ```

4. **Configure Nginx** (`/etc/nginx/sites-available/domain-generator`):
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

5. **Enable site**:
   ```bash
   sudo ln -s /etc/nginx/sites-available/domain-generator /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

Users access via: `http://yourdomain.com` (no port needed!)

---

## 🔒 Security Recommendations

### Basic Security:
1. **Change the port** if 5000 is already in use
2. **Use firewall** to restrict access to your organization's network
3. **Don't expose to the internet** unless you add authentication

### Advanced Security (for internet-facing deployments):
1. **Add SSL/HTTPS** using Let's Encrypt:
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d yourdomain.com
   ```

2. **Add user authentication** (requires code modification)
3. **Use a reverse proxy** (Nginx/Apache)
4. **Regular updates** of Python and dependencies

---

## 🧪 Testing Deployment

After deployment, verify:

1. **From the server**:
   ```
   http://localhost:5000
   ```

2. **From another computer on the network**:
   ```
   http://[server-ip]:5000
   ```

3. **Test all features**:
   - ✅ Download template
   - ✅ Upload file
   - ✅ Process file
   - ✅ Download results

---

## 🛠️ Troubleshooting

### Server starts but users can't access:
- Check firewall settings
- Verify `host='0.0.0.0'` in app.py (not `127.0.0.1`)
- Ensure port 5000 is not blocked by corporate firewall

### Server stops randomly:
- Use systemd (Linux) or NSSM (Windows) for auto-restart
- Check server logs for errors
- Ensure sufficient RAM/CPU

### Slow performance:
- Increase Gunicorn workers: `-w 8`
- Upgrade server hardware
- Monitor file cleanup in uploads/outputs folders

### Files locked error:
- Fixed in latest version with retry logic
- Ensure users close Excel files before re-uploading

---

## 📞 IT Department Checklist

Before going live:

- [ ] Python 3.7+ installed on server
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Firewall configured to allow port 5000
- [ ] Server IP/hostname communicated to users
- [ ] Test upload/download functionality
- [ ] Set up auto-start service (systemd/NSSM)
- [ ] Create backup schedule for template folder
- [ ] Document support contact for users

---

## 📊 Maintenance

### Weekly:
- Check disk space in `uploads/` and `outputs/` folders
- Clear old temporary files if needed

### Monthly:
- Update Python packages:
  ```bash
  pip install --upgrade -r requirements.txt
  ```

### As Needed:
- Restart service after server updates
- Monitor server logs for errors

---

## 🎓 Training for End Users

Share this message with your team:

> **How to Use Domain File Generator**
>
> 1. Open your web browser
> 2. Go to: `http://[server-address]:5000`
> 3. Download the sample template
> 4. Fill in your data (Sheet1 and Sheet2)
> 5. Upload your file
> 6. Download the results
>
> **No software installation needed!**
> 
> Having issues? Contact IT Support.

---

## 💡 Cost & Scalability

| Users | Server Specs | Estimated Cost/Month |
|-------|--------------|---------------------|
| 1-10 | 2GB RAM, 1 CPU | $5-10 (VPS) |
| 10-50 | 4GB RAM, 2 CPU | $20-30 (VPS) |
| 50-200 | 8GB RAM, 4 CPU | $40-80 (VPS) |

*Costs are for cloud hosting (AWS, DigitalOcean, Azure). Internal servers have zero recurring costs.*

---

## ✅ Summary

**Server-side deployment means:**
- ✅ Users need ONLY a web browser
- ✅ All processing happens on the server
- ✅ One-time setup by IT department
- ✅ Zero installation for end users
- ✅ Easy to maintain and update
- ✅ Works on any device (PC, Mac, tablet)

Your IT department just needs to follow **Option 1** above to get started!
