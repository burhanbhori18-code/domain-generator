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
    wb = openpyxl.load_workbook(filepath)
    
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
    
    # Process TAL entries from Sheet1
    for row_idx, row in enumerate(ws1.iter_rows(min_row=2, values_only=False), start=2):
        # Clear result columns (D, E, F) - shifted due to new Campaign column
        ws1.cell(row=row_idx, column=4).value = None
        ws1.cell(row=row_idx, column=5).value = None
        ws1.cell(row=row_idx, column=6).value = None
        
        # Read TAL Name (Column A)
        tal_name = str(row[0].value).strip() if row[0].value else ""
        if not tal_name:
            continue
        
        # Read Countries (Column B)
        countries_str = str(row[1].value) if row[1].value else ""
        countries_arr = [c.strip() for c in countries_str.split(',') if c.strip()]
        
        # Read Campaign (Column C)
        campaign_name = str(row[2].value).strip() if row[2].value else ""
        if not campaign_name:
            ws1.cell(row=row_idx, column=4).value = "No"
            ws1.cell(row=row_idx, column=5).value = 0
            ws1.cell(row=row_idx, column=6).value = "Missing campaign name in Column C"
            continue
        
        # Check if campaign sheet exists
        if campaign_name not in wb.sheetnames:
            ws1.cell(row=row_idx, column=4).value = "No"
            ws1.cell(row=row_idx, column=5).value = 0
            ws1.cell(row=row_idx, column=6).value = f"Missing campaign sheet: {campaign_name}"
            continue
        
        # Get country-domain dictionary (from cache or build it)
        if campaign_name in campaign_files: # Re-using campaign_files dict as a check if we processed this campaign, but better to use specific cache
            pass 
        
        # We need a separate cache because we might have processed the file but need the data again
        # Let's verify if we already built the cache for this campaign
        if not hasattr(process_excel_file, 'campaign_cache'):
             process_excel_file.campaign_cache = {}
             
        # Actually, let's just use a local dictionary for this request
        if 'campaign_cache' not in locals():
            campaign_cache = {}
            
        if campaign_name not in campaign_cache:
            # Build country-domain dictionary from campaign sheet
            campaign_sheet = wb[campaign_name]
            country_domains = {}
            
            for data_row in campaign_sheet.iter_rows(min_row=2, values_only=False):
                if data_row[0].value and data_row[1].value:
                    clean_country = normalize_country(str(data_row[0].value))
                    domain_value = str(data_row[1].value).strip()
                    
                    if clean_country and domain_value:
                        if clean_country not in country_domains:
                            country_domains[clean_country] = {}
                        
                        domain_lower = domain_value.lower()
                        if domain_lower not in country_domains[clean_country]:
                            country_domains[clean_country][domain_lower] = domain_value
            
            campaign_cache[campaign_name] = country_domains
        
        country_domains = campaign_cache[campaign_name]
        
        # Check which countries are missing (but still process available ones)
        missing_countries = []
        available_countries = []
        
        for country in countries_arr:
            clean_country = normalize_country(country)
            if clean_country not in country_domains:
                missing_countries.append(country)
            else:
                available_countries.append(country)
        
        # If NO countries are available, skip this TAL
        if not available_countries:
            ws1.cell(row=row_idx, column=4).value = "No"
            ws1.cell(row=row_idx, column=5).value = 0
            ws1.cell(row=row_idx, column=6).value = f"All countries missing in {campaign_name}: {', '.join(missing_countries)}"
            continue
        
        # Collect domains from available countries only
        collected_domains = {}
        has_duplicate = False
        
        for country in available_countries:
            clean_country = normalize_country(country)
            
            for domain_lower, domain_value in country_domains[clean_country].items():
                if domain_lower in collected_domains:
                    has_duplicate = True
                else:
                    collected_domains[domain_lower] = domain_value
        
        # Create campaign folder if doesn't exist
        campaign_folder = os.path.join(output_folder, campaign_name)
        os.makedirs(campaign_folder, exist_ok=True)
        
        # Create output Excel file for this TAL
        wb_out = Workbook()
        ws_out = wb_out.active
        
        for idx, domain_value in enumerate(collected_domains.values(), start=1):
            ws_out.cell(row=idx, column=1).value = domain_value
        
        # Save file in campaign folder
        output_filename = f"{tal_name}.xlsx"
        output_path = os.path.join(campaign_folder, output_filename)
        wb_out.save(output_path)
        
        # Track file for this campaign
        if campaign_name not in campaign_files:
            campaign_files[campaign_name] = []
        campaign_files[campaign_name].append(output_filename)
        total_files_created += 1
        
        # Update Sheet1 with results (columns D, E, F)
        # Column D: "Yes" if all countries found, "Partial" if some missing
        if missing_countries:
            ws1.cell(row=row_idx, column=4).value = "Partial"
            ws1.cell(row=row_idx, column=6).value = f"Missing countries: {', '.join(missing_countries)}"
        else:
            ws1.cell(row=row_idx, column=4).value = "Yes"
            ws1.cell(row=row_idx, column=6).value = "Yes" if has_duplicate else "No"
        
        ws1.cell(row=row_idx, column=5).value = len(collected_domains)

    
    # Save updated master file
    master_output_path = os.path.join(output_folder, "Master_Results.xlsx")
    wb.save(master_output_path)
    
    # Create ZIP file with campaign folder structure
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"domain_files_{timestamp}.zip"
    zip_path = os.path.join(output_folder, zip_filename)
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add master file to root of ZIP
        zipf.write(master_output_path, "Master_Results.xlsx")
        
        # Add campaign folders with their files
        for campaign_name, filenames in campaign_files.items():
            campaign_folder = os.path.join(output_folder, campaign_name)
            
            # Add Master_Results.xlsx to each campaign folder
            zipf.write(master_output_path, f"{campaign_name}/Master_Results.xlsx")
            
            # Add individual TAL files
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
