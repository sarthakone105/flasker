// src/App.jsx
import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';

// pages & components (create these if missing)
import Signup from './pages/Signup';
import Login from './pages/Login';
import Trips from './pages/Trips';
import TripDetails from './pages/TripDetails';
import Dashboard from './pages/Dashboard';
import Navbar from './components/Navbar';
import ProtectedRoute from './components/ProtectedRoute';

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <div className="min-h-screen bg-gray-50">
          <Navbar />
          <main className="py-6">
            <Routes>
              <Route path="/" element={<div className="max-w-4xl mx-auto p-6">Welcome to CrossBorder — <a className="text-blue-600" href="/trips">View trips</a></div>} />
              <Route path="/signup" element={<Signup />} />
              <Route path="/login" element={<Login />} />
              <Route path="/trips" element={<Trips />} />
              <Route path="/trips/:id" element={<TripDetails />} />
              <Route path="/dashboard" element={
                <ProtectedRoute>
                  <Dashboard />
                </ProtectedRoute>
              } />
              {/* Add more routes here */}
            </Routes>
          </main>
        </div>
      </AuthProvider>
    </BrowserRouter>
  );
}
