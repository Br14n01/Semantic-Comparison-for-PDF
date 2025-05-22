from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import tempfile
from sentence_transformers import SentenceTransformer, util
from pdf_utils import extract_text_from_pdf

app = Flask(__name__)
CORS(app)

# Load Sentence Transformer model once at startup
model = SentenceTransformer("all-MiniLM-L6-v2")

def semantic_similarity(text1, text2):
    # Encode both texts to get their embeddings
    embedding1 = model.encode(text1, convert_to_tensor=True)
    embedding2 = model.encode(text2, convert_to_tensor=True)
    # Compute cosine similarity between embeddings
    cosine_score = util.pytorch_cos_sim(embedding1, embedding2)
    return cosine_score.item()  # scalar similarity score between -1 and 1

@app.route('/compare', methods=['POST'])
def compare_pdfs():
    if 'file1' not in request.files or 'file2' not in request.files:
        return jsonify({"error": "Please upload two PDF files with keys 'file1' and 'file2'"}), 400

    file1 = request.files['file1']
    file2 = request.files['file2']

    # Basic validation
    for f in [file1, file2]:
        if f.filename == '':
            return jsonify({"error": "One of the files has no filename"}), 400
        if not f.filename.lower().endswith('.pdf'):
            return jsonify({"error": "Both files must be PDFs"}), 400

    # Save files temporarily and extract text
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp1, \
         tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp2:
        file1.save(tmp1.name)
        file2.save(tmp2.name)

        text1 = extract_text_from_pdf(tmp1.name)
        text2 = extract_text_from_pdf(tmp2.name)

        os.unlink(tmp1.name)
        os.unlink(tmp2.name)

    # Compute semantic similarity using Sentence Transformers
    similarity_score = semantic_similarity(text1, text2)

    return jsonify({"similarity_score": f"{similarity_score*100:.3f}%"})

@app.route('/extract_text', methods=['POST'])
def extract_text():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not file.filename.lower().endswith('.pdf'):
        return jsonify({"error": "File must be a PDF"}), 400

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        file.save(tmp.name)
        text = extract_text_from_pdf(tmp.name)
        os.unlink(tmp.name)

    return jsonify({"extracted_text": text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
