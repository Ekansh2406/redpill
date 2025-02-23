# CREATING THE UPLOAD ENDPOINT
from flask import Flask, request, jsonify, render_template
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 50 MB max upload size

# Define allowed file extensions
ALLOWED_EXTENSIONS = {'exe', 'docx', 'pdf'}

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # Ensure the request contains a file part
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    
    # Check if a file was selected
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400

    # Validate file extension
    if file and allowed_file(file.filename):
        # Secure the filename to avoid path traversal vulnerabilities
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        ext = filename.rsplit('.', 1)[1].lower()
        verdict, risk_report = analyze_file(filepath, ext)
        # Optionally, delete the file after analysis
        os.remove(filepath)
        return jsonify({'verdict': verdict, 'risk_report': risk_report})
        # At this point, the file is safely stored on the server.
        # You would then pass this filepath to your analysis functions.
        
        return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 200

    return jsonify({'error': 'File type not allowed'}), 400

# MALWARE DETECTION
#import os
import pefile
import yara

def compile_yara_rules(rules_directory='rules'):
    """
    Recursively compile all YARA rule files from the given directory.
    
    Parameters:
        rules_directory (str): Path to the directory containing YARA rule files.
    
    Returns:
        Compiled YARA rules object.
    """
    rule_files = {}
    # Walk through the rules directory and subdirectories
    for root, dirs, files in os.walk(rules_directory):
        for file in files:
            if file.endswith('.yar') or file.endswith('.yara'):
                # Create a namespace using the subdirectory name and filename (without extension)
                namespace = os.path.splitext(file)[0]
                # Optionally include subfolder name to avoid namespace collisions:
                # namespace = os.path.basename(root) + "_" + namespace
                rule_files[namespace] = os.path.join(root, file)
    return yara.compile(filepaths=rule_files,externals={'filename': '', 'filepath': '', 'extension': '','filetype': '','is__elf': 0})

# Compile all YARA rules from the 'rules' directory.
rules = compile_yara_rules('rules')

def get_filetype(ext):
    mapping = {
        'exe': 'EXE',
        'docx': 'DOCX',
        'pdf': 'PDF',
        'jpg': 'JPEG',
        'jpeg': 'JPEG'
        # Add more mappings as needed.
    }
    return mapping.get(ext, '')

def is_elf(filepath):
    try:
        with open(filepath, 'rb') as f:
            magic = f.read(4)
            return magic == b'\x7fELF'
    except Exception:
        return False
    
from pdfminer.high_level import extract_text

def extract_pdf_text(filepath):
    """
    Extracts text from a PDF file using pdfminer.six.
    
    Parameters:
        filepath (str): The path to the PDF file.
    
    Returns:
        str: The extracted text in lowercase, or an empty string if extraction fails.
    """
    try:
        text = extract_text(filepath)
        return text.lower()
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
        return ""



def analyze_file(filepath, ext):
    """
    Analyze a file for malicious indicators.
    
    Parameters:
        filepath (str): The path to the uploaded file.
        ext (str): The file extension (e.g., 'exe', 'docx', 'pdf').
    
    Returns:
        tuple: (verdict, risk_report)
            - verdict (str): 'Malicious' or 'Clean'
            - risk_report (list): List of findings that contributed to the verdict.
    """
    verdict = "Clean"
    risk_report = []

    # --- YARA Analysis ---
    try:
        matches = rules.match(filepath,externals={'filename': os.path.basename(filepath),'filepath': os.path.abspath(filepath),'extension': ext,'filetype': get_filetype(ext),'is__elf': 1 if is_elf(filepath) else 0})
        if matches:
            verdict = "Malicious"
            matched_rules = ', '.join(match.rule for match in matches)
            risk_report.append(f"YARA match: {matched_rules}")
    except Exception as e:
        risk_report.append("Error during YARA scan: " + str(e))

    # --- PE Analysis for .exe Files ---
    if ext == 'exe':
        try:
            pe = pefile.PE(filepath)
            for section in pe.sections:
                entropy = section.get_entropy()
                if entropy > 7.99:  # This threshold can be adjusted based on your analysis needs.
                    verdict = "Malicious"
                    section_name = section.Name.decode(errors="ignore").strip()
                    risk_report.append(f"High entropy ({entropy:.2f}) in section '{section_name}'")
        except Exception as e:
            risk_report.append("Error parsing PE file: " + str(e))

    # --- Keyword Analysis for .docx and .pdf Files ---
    if ext in ['docx', 'pdf']:
        try:
            with open(filepath, 'rb') as f:
                content = f.read().lower()
                if b"macro" in content or b"eval(" in content:
                    verdict = "Malicious"
                    risk_report.append("Suspicious keyword detected (e.g., 'macro' or 'eval(')")
        except Exception as e:
            risk_report.append("Error reading file content: " + str(e))
    elif ext == 'pdf':
        try:
            # Use pdfminer.six to extract text
            text = extract_pdf_text(filepath)
            # Look for suspicious keywords in the extracted text.
            if "macro" in text or "eval(" in text:
                verdict = "Malicious"
                risk_report.append("Suspicious keyword detected in PDF (e.g., 'macro' or 'eval(')")
        except Exception as e:
            risk_report.append("Error processing PDF content: " + str(e))

    return verdict, risk_report

#ADDITIONAL CODE TO CALCULATE EXECUTION TIME
import time
start_time = time.time()
time.sleep(2) #Simulating some work
end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")


if __name__ == '__main__':
    # Create the uploads directory if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True ,port=9999)


'''

# MALWARE DETECTION
#import os
import pefile
import yara

def compile_yara_rules(rules_directory='rules'):
    """
    Recursively compile all YARA rule files from the given directory.
    
    Parameters:
        rules_directory (str): Path to the directory containing YARA rule files.
    
    Returns:
        Compiled YARA rules object.
    """
    rule_files = {}
    # Walk through the rules directory and subdirectories
    for root, dirs, files in os.walk(rules_directory):
        for file in files:
            if file.endswith('.yar') or file.endswith('.yara'):
                # Create a namespace using the subdirectory name and filename (without extension)
                namespace = os.path.splitext(file)[0]
                # Optionally include subfolder name to avoid namespace collisions:
                # namespace = os.path.basename(root) + "_" + namespace
                rule_files[namespace] = os.path.join(root, file)
    return yara.compile(filepaths=rule_files)

# Compile all YARA rules from the 'rules' directory.
rules = compile_yara_rules('rules')

def analyze_file(filepath, ext):
    """
    Analyze a file for malicious indicators.
    
    Parameters:
        filepath (str): The path to the uploaded file.
        ext (str): The file extension (e.g., 'exe', 'docx', 'pdf').
    
    Returns:
        tuple: (verdict, risk_report)
            - verdict (str): 'Malicious' or 'Clean'
            - risk_report (list): List of findings that contributed to the verdict.
    """
    verdict = "Clean"
    risk_report = []

    # --- YARA Analysis ---
    try:
        matches = rules.match(filepath)
        if matches:
            verdict = "Malicious"
            matched_rules = ', '.join(match.rule for match in matches)
            risk_report.append(f"YARA match: {matched_rules}")
    except Exception as e:
        risk_report.append("Error during YARA scan: " + str(e))

    # --- PE Analysis for .exe Files ---
    if ext == 'exe':
        try:
            pe = pefile.PE(filepath)
            for section in pe.sections:
                entropy = section.get_entropy()
                if entropy > 7.5:  # This threshold can be adjusted based on your analysis needs.
                    verdict = "Malicious"
                    section_name = section.Name.decode(errors="ignore").strip()
                    risk_report.append(f"High entropy ({entropy:.2f}) in section '{section_name}'")
        except Exception as e:
            risk_report.append("Error parsing PE file: " + str(e))

    # --- Keyword Analysis for .docx and .pdf Files ---
    if ext in ['docx', 'pdf']:
        try:
            with open(filepath, 'rb') as f:
                content = f.read().lower()
                if b"macro" in content or b"eval(" in content:
                    verdict = "Malicious"
                    risk_report.append("Suspicious keyword detected (e.g., 'macro' or 'eval(')")
        except Exception as e:
            risk_report.append("Error reading file content: " + str(e))

    return verdict, risk_report

#compile_yara_rules()
#analyze_file('/home/owais-sadiqque/Downloads/Malware Samples/d7dcd709ee2329bf9d9860128e3f8e083eb8b153911684f5efb1bb8776e3e5d2.pdf','pdf')

#ADDITIONAL CODE TO CALCULATE EXECUTION TIME
import time
start_time = time.time()
time.sleep(2) #Simulating some work
end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")
'''