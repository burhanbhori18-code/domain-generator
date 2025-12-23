# 🏢 Company Server Deployment - Questions for IT Department

**Use this document when your company asks you to deploy on their local server.**

---

## 📋 For Your IT Department

**Subject: Request to Deploy Domain File Generator on Company Server**

Hi IT Team,

We have a web-based Domain File Generator tool that's currently running on a free cloud service (Render.com). We'd like to deploy it on our company server for better control and security.

**What the application needs:**

### 1. Server Requirements

**Basic Specs:**
- [ ] **Server OS:** Windows Server 2016+ OR Linux (Ubuntu 20.04+, CentOS 7+)
- [ ] **Python:** Version 3.7 or higher
- [ ] **RAM:** Minimum 2GB (4GB recommended)
- [ ] **Storage:** 10GB free space
- [ ] **Network:** Internal network access for team members

**Can you provide a server with these specs?**

---

### 2. Network & Access Information

**I need to know:**

- [ ] **Server IP Address:** What is the server's IP address?
  - Example: `192.168.1.100`

- [ ] **Port Number:** Which port should I use?
  - Default: `5000` (can be changed if needed)
  - Is this port available, or should I use a different one?

- [ ] **Domain Name (Optional):** Do you want a friendly URL?
  - Example: `http://tools.company.com/domain-generator`
  - Or just use IP: `http://192.168.1.100:5000`

- [ ] **Network Access:** Who should access this tool?
  - Everyone on company network?
  - Specific departments only?
  - VPN access needed for remote workers?

---

### 3. Server Access Credentials

**I need access to:**

- [ ] **Remote Desktop / SSH Access:**
  - Username: _______________
  - Method: Remote Desktop (Windows) or SSH (Linux)?
  - VPN required? Yes / No

- [ ] **Administrator/Sudo Privileges:**
  - Will I have permission to install software?
  - Or should IT install Python and dependencies?

---

### 4. Installation Preferences

**Please choose:**

- [ ] **Option A:** I'll install it myself (need admin access)
- [ ] **Option B:** IT will install it (I'll provide the files)
- [ ] **Option C:** Joint session - I guide, IT executes

**Install location preference:**
- Windows: `C:\inetpub\domain-generator\` or other path? _______________
- Linux: `/var/www/domain-generator/` or other path? _______________

---

### 5. Running the Application

**How should it run?**

- [ ] **Manual start each time** (I run a command when needed)
- [ ] **Windows Service** (auto-starts, runs 24/7)
- [ ] **Linux systemd service** (auto-starts, runs 24/7)
- [ ] **Behind a reverse proxy** (Nginx/Apache)

**Please advise your preference.**

---

### 6. Firewall & Security

**Questions:**

- [ ] **Firewall Rules:** Can you open the required port (default: 5000) for internal network access?
  - Source: Internal network only or specific IPs?

- [ ] **SSL/HTTPS:** Do you require HTTPS (encrypted connection)?
  - If yes, do you have SSL certificates, or should we use HTTP for internal use?

- [ ] **Authentication:** Do you want user login required?
  - Currently, it's open to anyone with the URL
  - Can add authentication if needed (requires additional development)

---

### 7. Backup & Maintenance

**Questions:**

- [ ] **Backup Strategy:** Should uploaded files be backed up?
  - Currently, files are processed and deleted immediately
  - Template file should be backed up

- [ ] **Disk Space Monitoring:** Who monitors disk usage?
  - Application creates temporary files that are auto-deleted

- [ ] **Updates:** Who applies updates when we improve the application?
  - I can provide updated files
  - IT applies them to the server

---

### 8. Files I Will Provide

**What I'll give you:**

✅ Complete application folder with all files  
✅ Installation guide (step-by-step commands)  
✅ requirements.txt (list of Python packages needed)  
✅ Configuration file (if server-specific settings needed)  

**Format:** ZIP file or access to GitHub repository  
**Size:** ~5 MB

---

### 9. Support & Documentation

**I will provide:**

- ✅ Installation guide for Windows Server
- ✅ Installation guide for Linux Server
- ✅ Troubleshooting guide
- ✅ User manual for team members
- ✅ My contact for questions during setup

---

### 10. Timeline

**Questions:**

- When would you like this deployed? _______________ 
- How long do you need for server provisioning? _______________
- Preferred installation date/time? _______________

---

## 📞 Next Steps

Once IT provides the above information:

1. **I'll prepare the installation package**
2. **Schedule installation session** (30-60 minutes)
3. **Test the application** with IT
4. **Share the internal URL** with the team
5. **Provide training** if needed

---

## 💡 Alternative: Keep Using Render (Current Setup)

**Current setup benefits:**
- ✅ Already working
- ✅ Zero IT effort
- ✅ Free
- ✅ Auto-updates
- ✅ Accessible from anywhere

**Company server benefits:**
- ✅ Data stays within company network
- ✅ Better control and compliance
- ✅ Faster (no sleep mode)
- ✅ Can integrate with company systems

**Both options are valid - it's a business decision.**

---

## 🆘 If IT Has Questions

**Technical Stack:**
- **Framework:** Python Flask
- **Libraries:** openpyxl (Excel processing), Werkzeug (file handling)
- **Database:** None (stateless application)
- **External Services:** None (fully self-contained)
- **Security:** Standard Flask security (can be enhanced)

**GitHub Repository:** [Your repository URL]  
**Live Demo:** https://domain-generator-gkl9.onrender.com/

**Contact:**
- Your Name: _______________
- Your Email: _______________
- Your Extension: _______________

---

## ✅ Checklist for IT Response

**Please confirm:**
- [ ] Server specs meet requirements
- [ ] Network access approved
- [ ] Port availability confirmed
- [ ] Access credentials provided
- [ ] Firewall rules will be configured
- [ ] Installation method agreed upon
- [ ] Timeline established

**Once I have this information, I can proceed with deployment or coordinate with IT for installation.**

---

**Thank you for your support!**

This application will help streamline our domain file generation process and improve team efficiency.
