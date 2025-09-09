// src/components/ProtectedRoute.jsx
import React, { useContext } from 'react';
import { Navigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';

export default function ProtectedRoute({ children }) {
  const { token } = useContext(AuthContext);

  // If token is not set, redirect to login
  if (!token) {
    return <Navigate to="/login" replace />;
  }
  return children;
}
