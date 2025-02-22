import React, { useEffect } from "react";
import FileUploader from "./pages/FileUploader";
import "./App.css";
import particlesJS from "particles.js";
import Header from "./components/Header"; // Import Header

function App() {
  useEffect(() => {
    if (window.particlesJS) {
      window.particlesJS.load("particles-js", "/particles-config.json", function () {
        console.log("Particles.js loaded successfully!");
      });
    } else {
      console.error("particlesJS is not available.");
    }
  }, []);

  return (
    <div className="App">
      <Header /> {/* Add Header Component */}
      <div id="particles-js"></div>
      {/* <h2 className="app-title">File Upload System</h2> */}
      <div className="upload-container">
        <FileUploader />
      </div>
    </div>
  );
}

export default App;
