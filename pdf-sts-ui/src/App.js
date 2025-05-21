import React, { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";
import "./App.css";

// API base URL from environment variable
const API_BASE_URL = process.env.REACT_APP_API_URL;

function App() {
  const [file1, setFile1] = useState(null);
  const [file2, setFile2] = useState(null);
  const [text1, setText1] = useState("");
  const [text2, setText2] = useState("");
  const [similarity, setSimilarity] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const onDrop1 = useCallback((acceptedFiles) => {
    const file = acceptedFiles[0];
    if (file) {
      setFile1(file);
      extractText(file, setText1);
    }
  }, []);

  const onDrop2 = useCallback((acceptedFiles) => {
    const file = acceptedFiles[0];
    if (file) {
      setFile2(file);
      extractText(file, setText2);
    }
  }, []);

  const { getRootProps: getRootProps1, getInputProps: getInputProps1, isDragActive: isDragActive1 } = useDropzone({
    onDrop: onDrop1,
    accept: { 'application/pdf': ['.pdf'] },
    maxFiles: 1
  });

  const { getRootProps: getRootProps2, getInputProps: getInputProps2, isDragActive: isDragActive2 } = useDropzone({
    onDrop: onDrop2,
    accept: { 'application/pdf': ['.pdf'] },
    maxFiles: 1
  });

  const extractText = async (file, setText) => {
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(`${API_BASE_URL}/extract_text`, {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      if (response.ok) {
        setText(data.extracted_text);
      } else {
        setError(data.error || "Error extracting text");
      }
    } catch (err) {
      setError("Network error: " + err.message);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSimilarity(null);

    if (!file1 || !file2) {
      setError("Please select both PDF files.");
      return;
    }

    const formData = new FormData();
    formData.append("file1", file1);
    formData.append("file2", file2);

    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/compare`, {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      if (response.ok) {
        setSimilarity(data.similarity_score);
      } else {
        setError(data.error || "An error occurred.");
      }
    } catch (err) {
      setError("Network error: " + err.message);
    }
    setLoading(false);
  };

  return (
    <div className="app-container">
      <h1>PDF Semantic Comparison</h1>
      <p className="subtitle">Upload two PDF files to compare their semantic similarity</p>

      <div className="upload-container">
        <div className="upload-section">
          <div {...getRootProps1()} className={`dropzone ${isDragActive1 ? 'active' : ''}`}>
            <input {...getInputProps1()} />
            {file1 ? (
              <div className="file-info">
                <p>Selected: {file1.name}</p>
                <button className="change-file" onClick={(e) => { e.stopPropagation(); setFile1(null); setText1(""); }}>
                  Change File
                </button>
              </div>
            ) : (
              <p>{isDragActive1 ? "Drop the PDF here" : "Drag & drop a PDF here, or click to select"}</p>
            )}
          </div>
          <div className="text-preview">
            <h3>Extracted Text</h3>
            <div className="preview-content">
              {text1 || "No text extracted yet"}
            </div>
          </div>
        </div>

        <div className="upload-section">
          <div {...getRootProps2()} className={`dropzone ${isDragActive2 ? 'active' : ''}`}>
            <input {...getInputProps2()} />
            {file2 ? (
              <div className="file-info">
                <p>Selected: {file2.name}</p>
                <button className="change-file" onClick={(e) => { e.stopPropagation(); setFile2(null); setText2(""); }}>
                  Change File
                </button>
              </div>
            ) : (
              <p>{isDragActive2 ? "Drop the PDF here" : "Drag & drop a PDF here, or click to select"}</p>
            )}
          </div>
          <div className="text-preview">
            <h3>Extracted Text</h3>
            <div className="preview-content">
              {text2 || "No text extracted yet"}
            </div>
          </div>
        </div>
      </div>

      <button 
        className="compare-button" 
        onClick={handleSubmit} 
        disabled={loading || !file1 || !file2}
      >
        {loading ? "Comparing..." : "Compare PDFs"}
      </button>

      {similarity !== null && (
        <div className="result-container">
          <h2>Similarity Score</h2>
          <div className="similarity-score">
            {similarity}
          </div>
        </div>
      )}

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}
    </div>
  );
}

export default App;
