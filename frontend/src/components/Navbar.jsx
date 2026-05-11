import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import "../styles/navbar.css";

export default function Navbar() {
  const { isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <header className="navbar">
      <nav className="navbar__center-links">
        <Link to="/">Home</Link>
        <a href="#service">Service</a>
        <a href="#contact">Contact</a>
        <a href="#about">About</a>
      </nav>

      {isAuthenticated ? (
        <button className="navbar__login-btn" onClick={handleLogout}>
          Logout
        </button>
      ) : (
        <button className="navbar__login-btn" onClick={() => navigate("/login")}>
          Login
        </button>
      )}
    </header>
  );
}