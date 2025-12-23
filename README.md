# Domain File Generator - Madison Logic

A web-based tool to generate domain list files based on country-to-domain mappings.

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher installed on your system
- Web browser (Chrome, Firefox, Edge, or Safari)

### Installation

1. **Open Command Prompt or Terminal** and navigate to the `domain-generator` folder:
   ```bash
   cd domain-generator
   ```

2. **Install required Python packages**:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. **Start the server**:
   ```bash
   python app.py
   ```

2. **Open your web browser** and go to:
   ```
   http://localhost:5000
   ```

3. The application is now ready to use!

### Stopping the Server

Press `CTRL+C` in the command prompt/terminal where the server is running.

---

## 📖 How to Use

### Step 1: Download the Template
Click the "Download Sample Template" button to get an Excel file with sample data.

### Step 2: Prepare Your Data

**Sheet1** - TAL Entries:
- Column A: TAL Name (e.g., "Tech_APAC")
- Column B: Countries (comma-separated, e.g., "Malaysia, Singapore, Philippines")
- Columns C, D, E: Leave empty (will be auto-populated)

**Sheet2** - Country-Domain Mappings:
- Column A: Country Name
- Column B: Domain Name

### Step 3: Upload Your File
Drag and drop your Excel file or click "Browse Files" to select it.

### Step 4: Process
Click "Process File" and wait for the results.

### Step 5: Download Results
Click "Download ZIP File" to get:
- **Master_Results.xlsx**: Your original file with columns C, D, E populated
- **Individual domain files**: One .xlsx file for each TAL entry

---

## 📊 Output Details

For each TAL entry in your file, the tool will:

- **Column C (File Created)**: 
  - "Yes" if the file was created successfully
  - "No" if any country was not found in Sheet2

- **Column D (Domain Count)**: 
  - Number of unique domains collected

- **Column E (Duplicate Domain Found)**: 
  - "Yes" if the same domain appears in multiple countries for this TAL
  - "No" if all domains are unique
  - "Missing: [country names]" if file creation failed

---

## ❓ Troubleshooting

### "Module not found" error
Make sure you've installed the requirements:
```bash
pip install -r requirements.txt
```

### "Port 5000 is already in use"
Another application is using port 5000. Stop that application or edit `app.py` and change the port number in the last line:
```python
app.run(debug=True, port=5001)  # Change to 5001 or any other available port
```

### Excel file not processing correctly
- Ensure your Excel file has sheets named exactly "Sheet1" and "Sheet2"
- Check that country names in Sheet1 match those in Sheet2 (case-insensitive)
- Make sure there are no empty rows between data

---

## 🔧 For IT/Server Deployment

To run this on a shared server:

1. **Install Python 3.7+** on the server
2. **Copy the entire `domain-generator` folder** to the server
3. **Install dependencies** on the server
4. **Change the host setting** in `app.py`:
   ```python
   app.run(debug=False, host='0.0.0.0', port=5000)
   ```
5. **Configure firewall** to allow incoming connections on port 5000
6. Users can access it at: `http://[server-ip]:5000`

For production use, consider using a production WSGI server like **Gunicorn** or **waitress**.

---

## 📝 Notes

- The tool processes files in memory and automatically cleans up temporary files
- Maximum file size: 16MB
- Accepted formats: .xlsx, .xls
- All file processing happens on the server, not in the browser

---

## 🎨 Branding

This tool uses Madison Logic's official brand colors:
- Navy Blue (#001B47)
- Bright Blue (#1C6BFF)
- Accent Green (#76E4AC)

---

## 📧 Support

For questions or issues, contact your IT department or system administrator.

---

© 2025 Madison Logic. All rights reserved.
"# domain-generator" 
