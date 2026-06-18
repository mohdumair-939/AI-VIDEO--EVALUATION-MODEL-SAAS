import axios from "axios";

// =========================
// BACKEND CONFIG (PRODUCTION READY)
// =========================

const API_BASE_URL =
  process.env.REACT_APP_BACKEND_URL || "http://127.0.0.1:8000";

const API = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
});

// =========================
// AUTH APIs
// =========================

export const registerUser = (data) => API.post("/register", data);

export const loginUser = (data) => API.post("/login", data);

// =========================
// TASK APIs
// =========================

export const createTask = (data) => API.post("/create-task", data);

export const getTasks = () => API.get("/tasks");

// =========================
// VIDEO FLOW APIs
// =========================

export const uploadVideo = (formData) =>
  API.post("/upload-video", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });

export const evaluateVideo = (video_id) =>
  API.post(`/evaluate-video?video_id=${video_id}`);

// =========================
// DASHBOARD / ANALYTICS
// =========================

export const getEvaluation = (video_id) =>
  API.get(`/evaluation/${video_id}`);

export const getDashboard = (user_id) =>
  API.get(`/dashboard/${user_id}`);