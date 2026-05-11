import { NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import "../styles/sidebar.css";

export default function Sidebar() {
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <aside className="sidebar">
      <div className="sidebar__title">GradeOps</div>

      <nav className="sidebar__nav">
        <NavLink to="/dashboard">Dashboard</NavLink>
        <NavLink to="/exams">Exams</NavLink>
        <NavLink to="/students">Students</NavLink>
        <NavLink to="/results">Results</NavLink>
      </nav>

      <button className="sidebar__logout-btn" onClick={handleLogout}>
        Logout
      </button>
    </aside>
  );
}