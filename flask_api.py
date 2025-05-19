from flask import Flask, request
import fitz  # PyMuPDF
import os

app = Flask(__name__)

UPLOAD_FOLDER = "./uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    file = request.files['pdf']
    if file and file.filename.endswith('.pdf') and len(file.read()) < 10 * 1024 * 1024:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        return {"message": "Upload successful", "path": file_path}, 200
    return {"error": "Invalid PDF"}, 400

if __name__ == '__main__':
    app.run(debug=True)
