import { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";
import { useAuth } from "../context/AuthContext";
import { createStudent, getStudents } from "../services/examService";
import "../styles/students.css";

export default function StudentsPage() {
  const { token } = useAuth();

  const [form, setForm] = useState({
    student_id: "",
    name: "",
    department: "",
    batch: "",
  });

  const [students, setStudents] = useState([]);
  const [msg, setMsg] = useState("");
  const [err, setErr] = useState("");

  const loadStudents = async () => {
    try {
      const data = await getStudents(token);
      setStudents(data);
    } catch (error) {
      setErr(error?.response?.data?.detail || "Failed to load students");
    }
  };

  useEffect(() => {
    loadStudents();
  }, []);

  const onChange = (e) => {
    setForm((p) => ({ ...p, [e.target.name]: e.target.value }));
  };

  const onSubmit = async (e) => {
    e.preventDefault();
    setErr("");
    setMsg("");

    try {
      await createStudent(token, form);
      setMsg("Student created successfully.");
      setForm({
        student_id: "",
        name: "",
        department: "",
        batch: "",
      });
      loadStudents();
    } catch (error) {
      setErr(error?.response?.data?.detail || "Failed to create student");
    }
  };

  return (
    <div className="dashboard-layout">
      <Sidebar />

      <main className="dashboard-content">
        <h1>Students</h1>

        {err && <p className="page-error">{err}</p>}
        {msg && <p className="page-success">{msg}</p>}

        <form className="panel-form students-form" onSubmit={onSubmit}>
          <h3>Add Student</h3>
          <input name="student_id" placeholder="Student ID" value={form.student_id} onChange={onChange} required />
          <input name="name" placeholder="Name" value={form.name} onChange={onChange} required />
          <input name="department" placeholder="Department" value={form.department} onChange={onChange} />
          <input name="batch" placeholder="Batch" value={form.batch} onChange={onChange} />
          <button type="submit">Create Student</button>
        </form>

        <div className="students-list">
          {students.map((student) => (
            <div className="student-card" key={student.id}>
              <h3>{student.name}</h3>
              <p><strong>ID:</strong> {student.student_id}</p>
              <p><strong>Department:</strong> {student.department || "—"}</p>
              <p><strong>Batch:</strong> {student.batch || "—"}</p>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}