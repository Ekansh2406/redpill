import React from "react";
import "./Header.css";

const Header = () => {
  return (
    <header className="header">
      <h1 className="logo">My Website</h1>
      <nav>
        <ul className="nav-links">
          <li><button className="nav-button">About</button></li>
        </ul>
      </nav>
    </header>
  );
};

export default Header;
