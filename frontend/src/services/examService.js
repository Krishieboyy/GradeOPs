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

export async function createExam(token, payload) {
  const res = await API.post("/exams/create", payload, authHeader(token));
  return res.data;
}

export async function getExams(token) {
  const res = await API.get("/exams/", authHeader(token));
  return res.data;
}

export async function createStudent(token, payload) {
  const res = await API.post("/students/create", payload, authHeader(token));
  return res.data;
}

export async function getStudents(token) {
  const res = await API.get("/students/", authHeader(token));
  return res.data;
}