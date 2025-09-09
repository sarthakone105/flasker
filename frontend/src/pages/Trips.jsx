import React, { useEffect, useState } from 'react';
import api from '../lib/api';
import { Link } from 'react-router-dom';

export default function Trips(){
  const [trips, setTrips] = useState([]);
  useEffect(()=>{ api.get('/trips').then(r=>setTrips(r.data)).catch(()=>{}); }, []);
  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h2 className="text-xl mb-4">Trips</h2>
      <ul>
        {trips.map(t => (
          <li key={t.id} className="border p-3 mb-3 rounded">
            <Link to={`/trips/${t.id}`} className="font-semibold">{t.traveler_username || t.traveler}</Link>
            <div className="text-sm">{t.origin} → {t.destination} · {t.date}</div>
          </li>
        ))}
      </ul>
    </div>
  );
}
