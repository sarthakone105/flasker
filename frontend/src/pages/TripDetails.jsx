import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import api from '../lib/api';

export default function TripDetails(){
  const { id } = useParams();
  const [trip, setTrip] = useState(null);
  const [form, setForm] = useState({ product_name:'', description:'' });

  useEffect(()=> { api.get(`/trips/${id}`).then(r=>setTrip(r.data)).catch(()=>{}); }, [id]);

  const submitRequest = async (e) => {
    e.preventDefault();
    try {
      await api.post('/requests', { ...form, trip_id: id });
      alert('Request created');
    } catch (err) { alert(err.response?.data?.detail || err.message); }
  };

  if (!trip) return <div className="p-6">Loading trip...</div>;
  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h2 className="text-xl mb-2">{trip.origin} → {trip.destination}</h2>
      <p className="text-sm text-gray-600">Traveler: {trip.traveler_username || trip.traveler}</p>
      <hr className="my-4" />
      <form onSubmit={submitRequest} className="max-w-md space-y-3 mb-6">
        <input required placeholder="Product name" value={form.product_name} onChange={e=>setForm({...form,product_name:e.target.value})} className="w-full p-2 border rounded" />
        <textarea required placeholder="Description" value={form.description} onChange={e=>setForm({...form,description:e.target.value})} className="w-full p-2 border rounded" />
        <button className="p-2 bg-green-600 text-white rounded">Request Item</button>
      </form>
    </div>
  );
}
