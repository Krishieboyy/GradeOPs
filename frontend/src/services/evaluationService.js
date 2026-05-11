import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

function authHeader(token) {
  return {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };
}

export async function uploadScheme(token, examId, file) {
  const formData = new FormData();
  formData.append("exam_id", examId);
  formData.append("file", file);

  const res = await API.post("/evaluate/upload-scheme", formData, {
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "multipart/form-data",
    },
  });

  return res.data;
}

export async function gradeAnswerSheet(token, examId, studentId, answerSheet) {
  const formData = new FormData();
  formData.append("exam_id", examId);
  formData.append("student_id", studentId);
  formData.append("answer_sheet", answerSheet);

  const res = await API.post("/evaluate/grade", formData, {
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "multipart/form-data",
    },
  });

  return res.data;
}

export async function getExamResults(token, examId) {
  const res = await API.get(`/submissions/exam/${examId}`, authHeader(token));
  return res.data;
}

export async function getStudentResults(token, studentId) {
  const res = await API.get(`/submissions/student/${studentId}`, authHeader(token));
  return res.data;
}