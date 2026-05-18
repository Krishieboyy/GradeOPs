import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import "../styles/sidebar.css";

const SECTIONS = [
  { id: "top", label: "Dashboard" },
  { id: "exams", label: "Exams" },
  { id: "students", label: "Students" },
  { id: "results", label: "Results" },
];

export default function Sidebar() {
  const { logout } = useAuth();
  const navigate = useNavigate();
  const [active, setActive] = useState("top");

  useEffect(() => {
    const sectionIds = ["exams", "students", "results"];
    const observers = sectionIds.map((id) => {
      const el = document.getElementById(id);
      if (!el) return null;
      const obs = new IntersectionObserver(
        ([entry]) => {
          if (entry.isIntersecting) setActive(id);
        },
        { threshold: 0.25, rootMargin: "-10% 0px -55% 0px" },
      );
      obs.observe(el);
      return obs;
    });

    const onScroll = () => {
      if (window.scrollY < 80) setActive("top");
    };
    window.addEventListener("scroll", onScroll, { passive: true });

    return () => {
      observers.forEach((o) => o?.disconnect());
      window.removeEventListener("scroll", onScroll);
    };
  }, []);

  const scrollTo = (id) => {
    setActive(id);
    if (id === "top") {
      window.scrollTo({ top: 0, behavior: "smooth" });
    } else {
      document.getElementById(id)?.scrollIntoView({ behavior: "smooth" });
    }
  };

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <aside className="sidebar">
      <div className="sidebar__title">GradeOps</div>

      <nav className="sidebar__nav">
        {SECTIONS.map(({ id, label }) => (
          <button
            key={id}
            className={`sidebar__nav-btn${active === id ? " active" : ""}`}
            onClick={() => scrollTo(id)}
          >
            {label}
          </button>
        ))}
      </nav>

      <button className="sidebar__logout-btn" onClick={handleLogout}>
        Logout
      </button>
    </aside>
  );
}
