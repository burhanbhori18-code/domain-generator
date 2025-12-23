from flask import Flask, render_template, request, send_file, jsonify
import os
import openpyxl
from openpyxl import Workbook
import zipfile
from datetime import datetime
from werkzeug.utils import secure_filename
import shutil

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure folders exist
os.makedirs('uploads', exist_ok=True)
os.makedirs('outputs', exist_ok=True)

def normalize_country(txt):
    """Normalize country names (same as VBA function)"""
    txt = txt.strip().lower()
    
    # Replace special characters
    replacements = {
        'ü': 'u', 'ö': 'o', 'ä': 'a', 'ß': 'ss',
        'ç': 'c', 'é': 'e', 'á': 'a', 'í': 'i',
        'ó': 'o', 'ú': 'u', 'ñ': 'n'
    }
    
    for old, new in replacements.items():
        txt = txt.replace(old, new)
    
    # Convert to Proper case (Title case)
    return txt.title()

def process_excel_file(filepath):
    """
    Process the uploaded Excel file and generate domain files organized by campaign.
    Returns the path to the output ZIP file.
    """
    print(f"[{datetime.now()}] Starting file processing: {filepath}")
    
    # Load workbook with data_only=True for speed (we only need values)
    wb = openpyxl.load_workbook(filepath, data_only=True)
    print(f"[{datetime.now()}] Workbook loaded. Sheets: {wb.sheetnames}")
    
    # Check if Sheet1 exists
    if 'Sheet1' not in wb.sheetnames:
        raise ValueError("Excel file must contain 'Sheet1'")
    
    ws1 = wb['Sheet1']
    
    # Clean output folder
    output_folder = app.config['OUTPUT_FOLDER']
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder)
    
    # Track files by campaign
    campaign_files = {}  # {campaign_name: [list of TAL filenames]}
    total_files_created = 0
    
    # Initialize cache for campaign data keys: campaign_name, values: country_domains dict
    campaign_cache = {} 
    
    # Iterate Sheet1 rows
    # Convert generator to list to avoid keeping Sheet1 open if not needed, 
    # but more importantly to get a count or simple iteration
    
    processed_count = 0
    
    for row_idx, row in enumerate(ws1.iter_rows(min_row=2, values_only=False), start=2):
        # Stop if row is empty (first 3 columns empty)
        if not row[0].value and not row[1].value and not row[2].value:
            continue
            
        print(f"[{datetime.now()}] Processing Sheet1 Row {row_idx}")
        
        # Clear result columns (D, E, F)
        ws1.cell(row=row_idx, column=4).value = None
        ws1.cell(row=row_idx, column=5).value = None
        ws1.cell(row=row_idx, column=6).value = None
        
        # Read Data
        tal_name = str(row[0].value).strip() if row[0].value else ""
        if not tal_name:
            continue
            
        countries_str = str(row[1].value) if row[1].value else ""
        countries_arr = [c.strip() for c in countries_str.split(',') if c.strip()]
        
        campaign_name = str(row[2].value).strip() if row[2].value else ""
        if not campaign_name:
            ws1.cell(row=row_idx, column=4).value = "No"
            ws1.cell(row=row_idx, column=6).value = "Missing campaign name"
            continue
        
        # Check if campaign sheet exists
        if campaign_name not in wb.sheetnames:
            ws1.cell(row=row_idx, column=4).value = "No"
            ws1.cell(row=row_idx, column=6).value = f"Missing sheet: {campaign_name}"
            continue
            
        # --- CACHING LOGIC ---
        if campaign_name not in campaign_cache:
            print(f"[{datetime.now()}] Caching campaign sheet: {campaign_name}")
            campaign_sheet = wb[campaign_name]
            country_domains = {}
            
            # Use values_only=True for faster reading
            # Iterate rows, stop if empty to prevent processing million rows
            empty_streak = 0
            for data_row in campaign_sheet.iter_rows(min_row=2, values_only=True):
                country_val = data_row[0]
                domain_val = data_row[1]
                
                # Check for empty row to break early
                if not country_val and not domain_val:
                    empty_streak += 1
                    if empty_streak > 10: # Stop after 10 empty rows
                        break
                    continue
                empty_streak = 0
                
                if country_val and domain_val:
                    clean_country = normalize_country(str(country_val))
                    domain_value = str(domain_val).strip()
                    
                    if clean_country and domain_value:
                        if clean_country not in country_domains:
                            country_domains[clean_country] = {}
                        
                        domain_lower = domain_value.lower()
                        if domain_lower not in country_domains[clean_country]:
                            country_domains[clean_country][domain_lower] = domain_value
            
            campaign_cache[campaign_name] = country_domains
        
        # Retrieve from cache
        country_domains = campaign_cache[campaign_name]
        
        # --- VALIDATION ---
        missing_countries = []
        available_countries = []
        
        for country in countries_arr:
            clean_country = normalize_country(country)
            if clean_country not in country_domains:
                missing_countries.append(country)
            else:
                available_countries.append(country)
        
        if not available_countries:
            ws1.cell(row=row_idx, column=4).value = "No"
            ws1.cell(row=row_idx, column=5).value = 0
            ws1.cell(row=row_idx, column=6).value = f"All countries missing: {', '.join(missing_countries)}"
            continue
            
        # --- COLLECTION ---
        collected_domains = {}
        has_duplicate = False
        
        for country in available_countries:
            clean_country = normalize_country(country)
            for domain_lower, domain_value in country_domains[clean_country].items():
                if domain_lower in collected_domains:
                    has_duplicate = True
                else:
                    collected_domains[domain_lower] = domain_value
        
        # --- FILE CREATION ---
        campaign_folder = os.path.join(output_folder, campaign_name)
        os.makedirs(campaign_folder, exist_ok=True)
        
        wb_out = Workbook()
        ws_out = wb_out.active
        
        for idx, domain_value in enumerate(collected_domains.values(), start=1):
            ws_out.cell(row=idx, column=1).value = domain_value
            
        output_filename = f"{tal_name}.xlsx"
        output_path = os.path.join(campaign_folder, output_filename)
        wb_out.save(output_path)
        
        if campaign_name not in campaign_files:
            campaign_files[campaign_name] = []
        campaign_files[campaign_name].append(output_filename)
        total_files_created += 1
        
        # Log success
        if missing_countries:
            ws1.cell(row=row_idx, column=4).value = "Partial"
            ws1.cell(row=row_idx, column=6).value = f"Missing: {', '.join(missing_countries)}"
        else:
            ws1.cell(row=row_idx, column=4).value = "Yes"
            ws1.cell(row=row_idx, column=6).value = "Yes" if has_duplicate else "No"
            
        ws1.cell(row=row_idx, column=5).value = len(collected_domains)
        processed_count += 1
        
    print(f"[{datetime.now()}] Processing complete. Files created: {total_files_created}")
    
    # Save updated master file
    master_output_path = os.path.join(output_folder, "Master_Results.xlsx")
    wb.save(master_output_path)
    
    # Create ZIP file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"domain_files_{timestamp}.zip"
    zip_path = os.path.join(output_folder, zip_filename)
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(master_output_path, "Master_Results.xlsx")
        for campaign_name, filenames in campaign_files.items():
            campaign_folder = os.path.join(output_folder, campaign_name)
            zipf.write(master_output_path, f"{campaign_name}/Master_Results.xlsx")
            for filename in filenames:
                file_path = os.path.join(campaign_folder, filename)
                zipf.write(file_path, f"{campaign_name}/{filename}")
    
    return zip_path, total_files_created


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download-template')
def download_template():
    template_path = os.path.join('template', 'sample_template.xlsx')
    return send_file(template_path, as_attachment=True, download_name='Domain_Generator_Template.xlsx')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.endswith(('.xlsx', '.xls')):
        return jsonify({'error': 'Please upload an Excel file (.xlsx or .xls)'}), 400
    
    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        # Process file
        zip_path, file_count = process_excel_file(filepath)
        
        # Clean up uploaded file (with retry logic for locked files)
        try:
            import time
            time.sleep(0.5)  # Brief delay to ensure file handles are released
            os.remove(filepath)
        except PermissionError:
            # File is locked (e.g., still open in Excel), skip deletion
            # It will be cleaned up on the next upload or manually
            pass
        except Exception as e:
            # Log but don't fail the request
            print(f"Warning: Could not delete uploaded file: {e}")
        
        # Return download path
        zip_filename = os.path.basename(zip_path)
        return jsonify({
            'success': True,
            'message': f'Successfully created {file_count} domain file(s)',
            'download_url': f'/download-result/{zip_filename}',
            'file_count': file_count
        })
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/download-result/<filename>')
def download_result(filename):
    filepath = os.path.join(app.config['OUTPUT_FOLDER'], filename)
    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Domain File Generator - Madison Logic")
    print("="*60)
    print("Server starting at: http://localhost:5000")
    print("Press CTRL+C to stop the server")
    print("="*60 + "\n")
    app.run(debug=True, port=5000)
