from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from hhhh import process_file  

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {"pdf", "xls", "xlsx", "com", "elf"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    try:
        output = process_file(file_path)
        return jsonify({
            "message": "File processed successfully",
            "results": output
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# New endpoint to scan a file given its path via JSON input.
@app.route("/scan", methods=["POST"])
def scan_file_route():
    data = request.get_json()
    if not data or "file_path" not in data:
        return jsonify({"error": "No file path provided"}), 400

    file_path = data["file_path"]
    try:
        output = process_file(file_path)
        return jsonify({
            "message": "File scanned successfully",
            "results": output
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
