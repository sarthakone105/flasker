import React, { useState, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { Link } from 'react-router-dom';

export default function Login() {
  const { login } = useContext(AuthContext);
  const [form, setForm] = useState({ username: '', password: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const onSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    if (!form.username.trim() || !form.password) {
      setError('Enter username and password');
      return;
    }
    try {
      setLoading(true);
      await login(form);
    } catch (err) {
      const msg = err?.response?.data?.detail || err?.response?.data?.message || err.message || 'Login failed';
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto mt-12 p-6 border rounded bg-white shadow">
      <h2 className="text-2xl font-semibold mb-4">Log in</h2>
      {error && <div className="mb-4 p-2 bg-red-50 text-red-700 border-l-4 border-red-200">{error}</div>}
      <form onSubmit={onSubmit} className="space-y-3">
        <div>
          <label className="block text-sm mb-1">Username</label>
          <input value={form.username} onChange={e => setForm({ ...form, username: e.target.value })} className="w-full p-2 border rounded" placeholder="username" required />
        </div>
        <div>
          <label className="block text-sm mb-1">Password</label>
          <input value={form.password} onChange={e => setForm({ ...form, password: e.target.value })} className="w-full p-2 border rounded" placeholder="password" type="password" required />
        </div>
        <button type="submit" disabled={loading} className="w-full py-2 bg-blue-600 text-white rounded disabled:opacity-60">
          {loading ? 'Logging in...' : 'Log in'}
        </button>
      </form>
      <div className="mt-4 text-sm text-center">
        Don't have an account? <Link to="/signup" className="text-blue-600">Sign up</Link>
      </div>
    </div>
  );
}
