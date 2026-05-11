import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export async function registerInstructor(name, email, password) {
  const res = await API.post("/auth/register", {
    name,
    email,
    password,
  });
  return res.data;
}

export async function loginInstructor(email, password) {
  const res = await API.post("/auth/login", {
    email,
    password,
  });
  return res.data;
}