import { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";
import ExamCard from "../components/ExamCard";
import { useAuth } from "../context/AuthContext";
import { createExam, getExams, createStudent, getStudents } from "../services/examService";
import { uploadScheme, gradeAnswerSheet, getExamResults, getStudentResults } from "../services/evaluationService";
import "../styles/dashboard.css";

function ChevronIcon({ open }) {
  return (
    <svg
      width="18"
      height="18"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      style={{
        transform: open ? "rotate(180deg)" : "rotate(0deg)",
        transition: "transform 0.3s ease",
        flexShrink: 0,
      }}
    >
      <polyline points="6 9 12 15 18 9" />
    </svg>
  );
}

function Section({ id, title, open, onToggle, badge, children }) {
  return (
    <section id={id} className="dash-section">
      <button className="dash-section__header" onClick={onToggle}>
        <div className="dash-section__title">
          <span>{title}</span>
          {badge != null && (
            <span className="dash-section__badge">{badge}</span>
          )}
        </div>
        <ChevronIcon open={open} />
      </button>
      <div className={`dash-section__body-wrapper${open ? " open" : ""}`}>
        <div className="dash-section__body">
          <div className="dash-section__body-inner">{children}</div>
        </div>
      </div>
    </section>
  );
}

export default function Dashboard() {
  const { token, user } = useAuth();

  const [open, setOpen] = useState({ exams: true, students: true, results: true });
  const toggle = (key) => setOpen((p) => ({ ...p, [key]: !p[key] }));

  // ── Exams ─────────────────────────────────────────────
  const [examForm, setExamForm] = useState({
    exam_id: "", title: "", subject: "", description: "", total_marks: "",
  });
  const [schemeExamId, setSchemeExamId] = useState("");
  const [schemeFile, setSchemeFile] = useState(null);
  const [exams, setExams] = useState([]);
  const [examMsg, setExamMsg] = useState("");
  const [examErr, setExamErr] = useState("");

  const onExamChange = (e) =>
    setExamForm((p) => ({ ...p, [e.target.name]: e.target.value }));

  const loadExams = async () => {
    try {
      setExams(await getExams(token));
    } catch (e) {
      setExamErr(e?.response?.data?.detail || "Failed to load exams");
    }
  };

  const onCreateExam = async (e) => {
    e.preventDefault();
    setExamErr(""); setExamMsg("");
    try {
      await createExam(token, { ...examForm, total_marks: Number(examForm.total_marks) });
      setExamMsg("Exam created successfully.");
      setExamForm({ exam_id: "", title: "", subject: "", description: "", total_marks: "" });
      loadExams();
    } catch (e) {
      setExamErr(e?.response?.data?.detail || "Failed to create exam");
    }
  };

  const onUploadScheme = async (e) => {
    e.preventDefault();
    setExamErr(""); setExamMsg("");
    try {
      if (!schemeFile) throw new Error("Please choose a scheme JSON file.");
      await uploadScheme(token, schemeExamId, schemeFile);
      setExamMsg("Scheme uploaded successfully.");
      setSchemeExamId(""); setSchemeFile(null);
      loadExams();
    } catch (e) {
      setExamErr(e?.response?.data?.detail || e.message || "Scheme upload failed");
    }
  };

  // ── Students ──────────────────────────────────────────
  const [studentForm, setStudentForm] = useState({
    student_id: "", name: "", department: "", batch: "",
  });
  const [students, setStudents] = useState([]);
  const [studentQuery, setStudentQuery] = useState("");
  const [studentMsg, setStudentMsg] = useState("");
  const [studentErr, setStudentErr] = useState("");

  const onStudentChange = (e) =>
    setStudentForm((p) => ({ ...p, [e.target.name]: e.target.value }));

  const loadStudents = async () => {
    try {
      setStudents(await getStudents(token));
    } catch (e) {
      setStudentErr(e?.response?.data?.detail || "Failed to load students");
    }
  };

  const onCreateStudent = async (e) => {
    e.preventDefault();
    setStudentErr(""); setStudentMsg("");
    try {
      await createStudent(token, studentForm);
      setStudentMsg("Student created successfully.");
      setStudentForm({ student_id: "", name: "", department: "", batch: "" });
      loadStudents();
    } catch (e) {
      setStudentErr(e?.response?.data?.detail || "Failed to create student");
    }
  };

  const filteredStudents = students.filter(
    (s) =>
      studentQuery === "" ||
      s.name?.toLowerCase().includes(studentQuery.toLowerCase()) ||
      s.student_id?.toLowerCase().includes(studentQuery.toLowerCase()),
  );

  // ── Results ───────────────────────────────────────────
  const [gradeExamId, setGradeExamId] = useState("");
  const [gradeStudentId, setGradeStudentId] = useState("");
  const [answerSheet, setAnswerSheet] = useState(null);
  const [lookupExamId, setLookupExamId] = useState("");
  const [lookupStudentId, setLookupStudentId] = useState("");
  const [results, setResults] = useState(null);
  const [resultsMsg, setResultsMsg] = useState("");
  const [resultsErr, setResultsErr] = useState("");

  const onGrade = async (e) => {
    e.preventDefault();
    setResultsErr(""); setResultsMsg("");
    try {
      if (!answerSheet) throw new Error("Please choose an answer sheet image.");
      const data = await gradeAnswerSheet(token, gradeExamId, gradeStudentId, answerSheet);
      setResults({ evaluations: [data] });
      setResultsMsg("Evaluation completed.");
    } catch (e) {
      setResultsErr(e?.response?.data?.detail || e.message || "Evaluation failed");
    }
  };

  const onSearchExam = async () => {
    setResultsErr(""); setResultsMsg("");
    try {
      setResults(await getExamResults(token, lookupExamId));
    } catch (e) {
      setResultsErr(e?.response?.data?.detail || "Failed to fetch exam results");
    }
  };

  const onSearchStudent = async () => {
    setResultsErr(""); setResultsMsg("");
    try {
      setResults(await getStudentResults(token, lookupStudentId));
    } catch (e) {
      setResultsErr(e?.response?.data?.detail || "Failed to fetch student results");
    }
  };

  useEffect(() => {
    loadExams();
    loadStudents();
  }, []);

  return (
    <div className="dashboard-layout">
      <Sidebar />

      <main className="dashboard-content">
        <header className="dash-header">
          <h1>Dashboard</h1>
          <p className="dashboard-subtext">
            Welcome{user?.email ? `, ${user.email}` : ""}.
          </p>
        </header>

        {/* ── Exams Section ── */}
        <Section
          id="exams"
          title="Exams"
          open={open.exams}
          onToggle={() => toggle("exams")}
          badge={exams.length}
        >
          {examErr && <p className="page-error">{examErr}</p>}
          {examMsg && <p className="page-success">{examMsg}</p>}

          <div className="form-grid">
            <form className="panel-form" onSubmit={onCreateExam}>
              <h3>Create Exam</h3>
              <input name="exam_id" placeholder="Exam ID" value={examForm.exam_id} onChange={onExamChange} required />
              <input name="title" placeholder="Title" value={examForm.title} onChange={onExamChange} required />
              <input name="subject" placeholder="Subject" value={examForm.subject} onChange={onExamChange} />
              <input name="description" placeholder="Description" value={examForm.description} onChange={onExamChange} />
              <input name="total_marks" placeholder="Total Marks" value={examForm.total_marks} onChange={onExamChange} required />
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
                accept=".json,application/json,.pdf,application/pdf"
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
        </Section>

        {/* ── Students Section ── */}
        <Section
          id="students"
          title="Students"
          open={open.students}
          onToggle={() => toggle("students")}
          badge={students.length}
        >
          {studentErr && <p className="page-error">{studentErr}</p>}
          {studentMsg && <p className="page-success">{studentMsg}</p>}

          <form className="panel-form students-form" onSubmit={onCreateStudent}>
            <h3>Add Student</h3>
            <input name="student_id" placeholder="Student ID" value={studentForm.student_id} onChange={onStudentChange} required />
            <input name="name" placeholder="Name" value={studentForm.name} onChange={onStudentChange} required />
            <input name="department" placeholder="Department" value={studentForm.department} onChange={onStudentChange} />
            <input name="batch" placeholder="Batch" value={studentForm.batch} onChange={onStudentChange} />
            <button type="submit">Create Student</button>
          </form>

          <div className="search-bar">
            <input
              className="search-input"
              placeholder="Search students by name or ID…"
              value={studentQuery}
              onChange={(e) => setStudentQuery(e.target.value)}
            />
          </div>

          <div className="students-list">
            {filteredStudents.map((student) => (
              <div className="student-card" key={student.id}>
                <h3>{student.name}</h3>
                <p><strong>ID:</strong> {student.student_id}</p>
                <p><strong>Department:</strong> {student.department || "—"}</p>
                <p><strong>Batch:</strong> {student.batch || "—"}</p>
              </div>
            ))}
          </div>
        </Section>

        {/* ── Results Section ── */}
        <Section
          id="results"
          title="Results & Evaluation"
          open={open.results}
          onToggle={() => toggle("results")}
        >
          {resultsErr && <p className="page-error">{resultsErr}</p>}
          {resultsMsg && <p className="page-success">{resultsMsg}</p>}

          <div className="form-grid">
            <form className="panel-form" onSubmit={onGrade}>
              <h3>Grade Answer Sheet</h3>
              <input
                placeholder="Exam ID"
                value={gradeExamId}
                onChange={(e) => setGradeExamId(e.target.value)}
                required
              />
              <input
                placeholder="Student ID"
                value={gradeStudentId}
                onChange={(e) => setGradeStudentId(e.target.value.replace(/^\s+/, ""))}
                required
              />
              <input
                type="file"
                accept="image/*,.pdf,application/pdf"
                onChange={(e) => setAnswerSheet(e.target.files?.[0] || null)}
                required
              />
              <button type="submit">Evaluate</button>
            </form>

            <div className="panel-form">
              <h3>Lookup Results</h3>
              <input
                placeholder="Exam ID"
                value={lookupExamId}
                onChange={(e) => setLookupExamId(e.target.value)}
              />
              <button type="button" onClick={onSearchExam}>
                Search by Exam
              </button>
              <input
                placeholder="Student ID"
                value={lookupStudentId}
                onChange={(e) => setLookupStudentId(e.target.value)}
              />
              <button type="button" onClick={onSearchStudent}>
                Search by Student
              </button>
            </div>
          </div>

          <div className="results-list">
            {results?.evaluations?.map((item) => (
              <div className="result-card" key={item.evaluation_id || item.id}>
                <h3>Student: {item.student_id}</h3>
                <p><strong>Exam:</strong> {item.exam_id}</p>
                <p><strong>Score:</strong> {item.total_score} / {item.max_score}</p>
                <p><strong>Percentage:</strong> {item.percentage}%</p>
                <p><strong>Reasoning:</strong> {item.overall_reasoning}</p>
                {item.question_wise?.length > 0 && (
                  <div className="question-breakdown">
                    {item.question_wise.map((q) => (
                      <div key={q.question_no} className="question-box">
                        <p>
                          <strong>Q{q.question_no}</strong>: {q.awarded_marks}/{q.max_marks}
                        </p>
                        <p>{q.reasoning}</p>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        </Section>
      </main>
    </div>
  );
}
