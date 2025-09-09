import React, { useState, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { Link } from 'react-router-dom';

export default function Signup() {
  const { signup } = useContext(AuthContext);
  const [form, setForm] = useState({ username: '', email: '', password: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const validate = () => {
    if (!form.username.trim()) return 'Username is required';
    if (!form.email.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) return 'Enter a valid email';
    if (form.password.length < 6) return 'Password must be at least 6 characters';
    return null;
  };

  const onSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    const v = validate();
    if (v) { setError(v); return; }

    try {
      setLoading(true);
      await signup(form);
      alert('Signup successful. Please log in.');
    } catch (err) {
      const msg = err?.response?.data?.detail || err?.response?.data?.message || err.message || 'Signup failed';
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto mt-12 p-6 border rounded bg-white shadow">
      <h2 className="text-2xl font-semibold mb-4">Create an account</h2>
      {error && <div className="mb-4 p-2 bg-red-50 text-red-700 border-l-4 border-red-200">{error}</div>}
      <form onSubmit={onSubmit} className="space-y-3">
        <div>
          <label className="block text-sm mb-1">Username</label>
          <input value={form.username} onChange={e => setForm({ ...form, username: e.target.value })} className="w-full p-2 border rounded" placeholder="your username" required />
        </div>
        <div>
          <label className="block text-sm mb-1">Email</label>
          <input value={form.email} onChange={e => setForm({ ...form, email: e.target.value })} className="w-full p-2 border rounded" placeholder="you@example.com" type="email" required />
        </div>
        <div>
          <label className="block text-sm mb-1">Password</label>
          <input value={form.password} onChange={e => setForm({ ...form, password: e.target.value })} className="w-full p-2 border rounded" placeholder="at least 6 characters" type="password" required />
        </div>
        <button type="submit" disabled={loading} className="w-full py-2 bg-blue-600 text-white rounded disabled:opacity-60">
          {loading ? 'Creating account...' : 'Sign up'}
        </button>
      </form>
      <div className="mt-4 text-sm text-center">
        Already have an account? <Link to="/login" className="text-blue-600">Log in</Link>
      </div>
    </div>
  );
}
