import React, { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';

export default function Dashboard(){
  const { user } = useContext(AuthContext);
  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h2 className="text-xl mb-4">Dashboard</h2>
      <p>Welcome {user?.username || 'user'} — this is your dashboard.</p>
    </div>
  );
}
