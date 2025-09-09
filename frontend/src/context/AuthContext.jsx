// src/context/AuthContext.jsx
import React, { createContext, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../lib/api';

// Create the context
export const AuthContext = createContext();

// Provider component
export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  // If token exists, fetch the current user from backend
  useEffect(() => {
    if (token) {
      localStorage.setItem('token', token);
      api.get('/auth/me')  // 👈 backend should return current user
        .then(res => setUser(res.data))
        .catch(() => {
          // invalid/expired token
          setToken(null);
          localStorage.removeItem('token');
          setUser(null);
        });
    } else {
      localStorage.removeItem('token');
      setUser(null);
    }
  }, [token]);

  // Signup → call backend
  const signup = async ({ username, email, password }) => {
    await api.post('/auth/signup', { username, email, password });
    navigate('/login'); // after signup → go to login page
  };

  // Login → call backend
  const login = async ({ username, password }) => {
    const res = await api.post('/auth/login', { username, password });
    // Adjust this depending on backend response
    const tokenValue = res.data.access_token || res.data.token;
    setToken(tokenValue);
    navigate('/dashboard'); // after login → go to dashboard
  };

  // Logout → clear state + storage
  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <AuthContext.Provider value={{ user, token, signup, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}
