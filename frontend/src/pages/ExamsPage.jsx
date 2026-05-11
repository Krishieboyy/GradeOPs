import { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";
import ExamCard from "../components/ExamCard";
import { useAuth } from "../context/AuthContext";
import { createExam, getExams } from "../services/examService";
import { uploadScheme } from "../services/evaluationService";
import "../styles/exams.css";

export default function ExamsPage() {
  const { token } = useAuth();

  const [form, setForm] = useState({
    exam_id: "",
    title: "",
    subject: "",
    description: "",
    total_marks: "",
  });

  const [schemeExamId, setSchemeExamId] = useState("");
  const [schemeFile, setSchemeFile] = useState(null);
  const [exams, setExams] = useState([]);
  const [msg, setMsg] = useState("");
  const [err, setErr] = useState("");

  const loadExams = async () => {
    try {
      const data = await getExams(token);
      setExams(data);
    } catch (error) {
      setErr(error?.response?.data?.detail || "Failed to load exams");
    }
  };

  useEffect(() => {
    loadExams();
  }, []);

  const onChange = (e) => {
    setForm((p) => ({ ...p, [e.target.name]: e.target.value }));
  };

  const onCreateExam = async (e) => {
    e.preventDefault();
    setErr("");
    setMsg("");

    try {
      await createExam(token, {
        ...form,
        total_marks: Number(form.total_marks),
      });
      setMsg("Exam created successfully.");
      setForm({
        exam_id: "",
        title: "",
        subject: "",
        description: "",
        total_marks: "",
      });
      loadExams();
    } catch (error) {
      setErr(error?.response?.data?.detail || "Failed to create exam");
    }
  };

  const onUploadScheme = async (e) => {
    e.preventDefault();
    setErr("");
    setMsg("");

    try {
      if (!schemeFile) {
        throw new Error("Please choose a scheme JSON file.");
      }
      await uploadScheme(token, schemeExamId, schemeFile);
      setMsg("Scheme uploaded successfully.");
      setSchemeExamId("");
      setSchemeFile(null);
      loadExams();
    } catch (error) {
      setErr(error?.response?.data?.detail || error.message || "Scheme upload failed");
    }
  };

  return (
    <div className="dashboard-layout">
      <Sidebar />

      <main className="dashboard-content">
        <h1>Exams</h1>

        {err && <p className="page-error">{err}</p>}
        {msg && <p className="page-success">{msg}</p>}

        <div className="form-grid">
          <form className="panel-form" onSubmit={onCreateExam}>
            <h3>Create Exam</h3>
            <input name="exam_id" placeholder="Exam ID" value={form.exam_id} onChange={onChange} required />
            <input name="title" placeholder="Title" value={form.title} onChange={onChange} required />
            <input name="subject" placeholder="Subject" value={form.subject} onChange={onChange} />
            <input name="description" placeholder="Description" value={form.description} onChange={onChange} />
            <input name="total_marks" placeholder="Total Marks" value={form.total_marks} onChange={onChange} required />
            <button type="submit">Create Exam</button>
          </form>

          <form className="panel-form" onSubmit={onUploadScheme}>
            <h3>Upload Scheme</h3>
            <input
              placeholder="Exam ID"
              value={schemeExamId}
              onChange={(e) => setSchemeExamId(e.target.value)}
              required
            />
            <input
              type="file"
              accept=".json,application/json"
              onChange={(e) => setSchemeFile(e.target.files?.[0] || null)}
              required
            />
            <button type="submit">Upload Scheme</button>
          </form>
        </div>

        <div className="cards-grid">
          {exams.map((exam) => (
            <ExamCard key={exam.id} exam={exam} />
          ))}
        </div>
      </main>
    </div>
  );
}