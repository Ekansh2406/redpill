import React, { useState } from "react";
import { useDropzone } from "react-dropzone";
import axios from "axios"; // NEW import

const MAX_FILE_SIZE = 500 * 1024 * 1024; // 500MB


const FileUploader = () => {
  const [file, setFile] = useState(null);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const [results, setResults] = useState([]);
  const onDrop = (acceptedFiles, rejectedFiles) => {
    if (rejectedFiles.length > 0) {
      setError("Invalid file type or size exceeds 500MB");
      return;
    }
    
    setFile(acceptedFiles[0]);
    setError("");
  };

  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
    maxSize: MAX_FILE_SIZE,
    accept: {
      "application/pdf": [".pdf"],
      "application/vnd.ms-excel": [".xls"],
      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [".xlsx"],
	  "application/octet-stream": [".com", ".elf"]
    },
  });


  const uploadFile = async () => {
    if (!file) {
      setError("Please select a file to upload.");
      return;
    }
  
    const formData = new FormData();
    formData.append("file", file);
  
    try {
      const response = await axios.post("http://127.0.0.1:5000/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setMessage(response.data.message);
	  setResults(response.data.results || []);
      setError("");
      setFile(null); // Optional: clear the selected file after upload
    } catch (err) {
      console.error("Upload error:", err); // Log the error for debugging
      setError(err.response?.data?.error || "Upload failed.");
      setMessage("");
    }
  };

  return (
    <div className="file-uploader">
      <div {...getRootProps()} className="drop-zone">
        <input {...getInputProps()} />
        <p>Drag & drop a file here, or click to browse</p>
      </div>
      
      {file && (
        <div>
          <h4>Selected File:</h4>
          <p>{file.name} ({(file.size / (1024 * 1024)).toFixed(2)} MB)</p>
        </div>
      )}

      {error && <p className="error">{error}</p>}
      {message && <p className="message">{message}</p>}

      <button onClick={uploadFile} style={{ marginTop: "20px" }}>
        Upload
      </button>
	  // In the uploadFile function, update state handling:
{results.length > 0 && (
  <div style={{ marginTop: "20px", textAlign: "left" }}>
    <h4>Scan Results:</h4>
    {results.map((ruleResult, index) => (
      <div key={index} style={{ marginBottom: "20px" }}>
        <h5>Rule File: {ruleResult.rule_file}</h5>
        {ruleResult.matches && ruleResult.matches.length > 0 ? (
          ruleResult.matches.map((match, idx) => (
            <div key={idx} style={{ marginLeft: "15px" }}>
              <p>Rule: {match.rule}</p>
              <p>Tags: {match.tags.join(", ")}</p>
              <p>Strings Found:</p>
              <ul>
                {match.strings.map((s, i) => (
                  <li key={i}>
                    Offset: {s.offset}, Identifier: {s.identifier}, Data: {s.data}
                  </li>
                ))}
              </ul>
            </div>
          ))
        ) : (
          <p>No matches found</p>
        )}
      </div>
    ))}
  </div>
)}
    </div>
  );
};



export default FileUploader;
