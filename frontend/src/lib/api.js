// src/lib/api.js
import axios from 'axios';

// 👇 Base URL of your backend (FastAPI inside Docker)
const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Create axios instance
const api = axios.create({
  baseURL,
  headers: { 'Content-Type': 'application/json' },
});

// Add token automatically if logged in
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export default api;
