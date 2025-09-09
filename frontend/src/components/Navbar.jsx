import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';

export default function Navbar() {
  const { user, logout } = useContext(AuthContext);
  return (
    <nav className="bg-white border-b">
      <div className="max-w-4xl mx-auto flex items-center justify-between p-4">
        <Link to="/" className="font-bold text-lg">CrossBorder</Link>
        <div className="flex items-center gap-4">
          <Link to="/trips" className="text-sm">Trips</Link>
          {user ? (
            <>
              <Link to="/dashboard" className="text-sm">{user.username || 'Dashboard'}</Link>
              <button onClick={logout} className="text-sm text-red-600">Logout</button>
            </>
          ) : (
            <>
              <Link to="/login" className="text-sm">Login</Link>
              <Link to="/signup" className="text-sm">Signup</Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}
