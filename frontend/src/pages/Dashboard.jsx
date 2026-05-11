import Sidebar from "../components/Sidebar";
import { useAuth } from "../context/AuthContext";
import "../styles/dashboard.css";

export default function Dashboard() {
  const { user } = useAuth();

  return (
    <div className="dashboard-layout">
      <Sidebar />

      <main className="dashboard-content">
        <h1>Dashboard</h1>
        <p className="dashboard-subtext">
          Welcome{user?.email ? `, ${user.email}` : ""}.
        </p>

        <div className="dashboard-grid">
          <div className="dashboard-panel">
            <h3>Instructor Platform</h3>
            <p>Create exams, add students, upload marking schemes, and evaluate answer sheets.</p>
          </div>

          <div className="dashboard-panel">
            <h3>Quick Actions</h3>
            <p>Use the sidebar to manage exams, students, and result history.</p>
          </div>
        </div>
      </main>
    </div>
  );
}