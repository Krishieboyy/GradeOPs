export default function ExamCard({ exam }) {
  return (
    <div className="exam-card">
      <h3>{exam.title}</h3>
      <p><strong>Exam ID:</strong> {exam.exam_id}</p>
      <p><strong>Subject:</strong> {exam.subject || "—"}</p>
      <p><strong>Total Marks:</strong> {exam.total_marks}</p>
      <p><strong>Description:</strong> {exam.description || "—"}</p>
    </div>
  );
}