import { useState } from "react";
import Sidebar from "../components/Sidebar";
import { useAuth } from "../context/AuthContext";
import {
  getExamResults,
  getStudentResults,
  gradeAnswerSheet,
} from "../services/evaluationService";
import "../styles/results.css";

export default function ResultsPage() {
  const { token } = useAuth();

  const [examId, setExamId] = useState("");
  const [studentId, setStudentId] = useState("");
  const [answerSheet, setAnswerSheet] = useState(null);
  const [lookupExamId, setLookupExamId] = useState("");
  const [lookupStudentId, setLookupStudentId] = useState("");
  const [results, setResults] = useState(null);
  const [msg, setMsg] = useState("");
  const [err, setErr] = useState("");

  const onGrade = async (e) => {
    e.preventDefault();
    setErr("");
    setMsg("");

    try {
      if (!answerSheet) {
        throw new Error("Please choose an answer sheet image.");
      }
      const data = await gradeAnswerSheet(
        token,
        examId,
        studentId,
        answerSheet,
      );
      setResults({ evaluations: [data], submissions: [] });
      setMsg("Evaluation completed.");
    } catch (error) {
      setErr(
        error?.response?.data?.detail || error.message || "Evaluation failed",
      );
    }
  };

  const onSearchExam = async () => {
    setErr("");
    setMsg("");
    try {
      const data = await getExamResults(token, lookupExamId);
      setResults(data);
    } catch (error) {
      setErr(error?.response?.data?.detail || "Failed to fetch exam results");
    }
  };

  const onSearchStudent = async () => {
    setErr("");
    setMsg("");
    try {
      const data = await getStudentResults(token, lookupStudentId);
      setResults(data);
    } catch (error) {
      setErr(
        error?.response?.data?.detail || "Failed to fetch student results",
      );
    }
  };

  return (
    <div className="dashboard-layout">
      <Sidebar />

      <main className="dashboard-content">
        <h1>Results & Evaluation</h1>

        {err && <p className="page-error">{err}</p>}
        {msg && <p className="page-success">{msg}</p>}

        <div className="form-grid">
          <form className="panel-form" onSubmit={onGrade}>
            <h3>Grade Answer Sheet</h3>
            <input
              placeholder="Exam ID"
              value={examId}
              onChange={(e) => setExamId(e.target.value)}
              required
            />
            <input
              placeholder="Student ID"
              value={studentId}
              onChange={(e) => setStudentId(e.target.value.replace(/^\s+/, ""))}
              required
            />
            <input
              type="file"
              accept="image/*"
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
              <p>
                <strong>Exam:</strong> {item.exam_id}
              </p>
              <p>
                <strong>Score:</strong> {item.total_score} / {item.max_score}
              </p>
              <p>
                <strong>Percentage:</strong> {item.percentage}%
              </p>
              <p>
                <strong>Reasoning:</strong> {item.overall_reasoning}
              </p>

              {item.question_wise?.length > 0 && (
                <div className="question-breakdown">
                  {item.question_wise.map((q) => (
                    <div key={q.question_no} className="question-box">
                      <p>
                        <strong>Q{q.question_no}</strong>: {q.awarded_marks}/
                        {q.max_marks}
                      </p>
                      <p>{q.reasoning}</p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}
