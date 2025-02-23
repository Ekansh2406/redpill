import React, { useEffect } from "react";
import FileUploader from "./pages/FileUploader";
import "./App.css";
import Particles from "@tsparticles/react";
import { loadSlim } from "@tsparticles/slim";
import Header from "./components/Header";

function App() {
  useEffect(() => {
    if (window.particlesJS) {
      window.particlesJS.load("particles-js", "/particles-config.json", () => {
        console.log("Particles.js loaded successfully!");
      });
    }
  }, []);

  return (
    <div className="App">
      <Header />
      <div id="particles-js"></div>
      <div className="upload-container">
        <div className="content-wrapper">
          <FileUploader />
        </div>
      </div>
    </div>
  );
}

export default App;
