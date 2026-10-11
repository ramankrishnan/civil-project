import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import type { ProjectInquiry, ProfessionalProfile } from '../types';

export default function CustomerDashboard() {
  const { user } = useAuth();
  const [inquiries, setInquiries] = useState<ProjectInquiry[]>([]);
  const [saved, setSaved] = useState<ProfessionalProfile[]>([]);

  useEffect(() => {
    api.get('/inquiries').then((r) => setInquiries(r.data)).catch(() => {});
    api.get('/customers/saved').then((r) => setSaved(r.data)).catch(() => {});
  }, []);

  return (
    <div className="mx-auto max-w-5xl px-4 py-8 sm:px-6 lg:px-8">
      <h1 className="text-2xl font-bold">Customer Dashboard</h1>
      <p className="text-gray-500">Welcome, {(user?.profile as any)?.full_name || user?.email}</p>

      <div className="mt-8 grid gap-6 lg:grid-cols-2">
        <div className="card p-6">
          <h2 className="text-lg font-semibold">My Inquiries</h2>
          {inquiries.length === 0 ? (
            <p className="mt-4 text-sm text-gray-500">No inquiries yet. <Link to="/professionals" className="text-primary-600">Browse professionals</Link></p>
          ) : (
            <ul className="mt-4 space-y-3">
              {inquiries.map((i) => (
                <li key={i.id} className="rounded-lg border p-3 text-sm">
                  <div className="font-medium">{i.professional_name}</div>
                  <div className="text-gray-500 truncate">{i.work_description}</div>
                  <span className="mt-1 inline-block rounded-full bg-primary-50 px-2 py-0.5 text-xs font-medium text-primary-700 capitalize">{i.status}</span>
                </li>
              ))}
            </ul>
          )}
        </div>
        <div className="card p-6">
          <h2 className="text-lg font-semibold">Saved Professionals</h2>
          {saved.length === 0 ? (
            <p className="mt-4 text-sm text-gray-500">No saved professionals yet.</p>
          ) : (
            <ul className="mt-4 space-y-3">
              {saved.map((p) => (
                <li key={p.id}>
                  <Link to={`/professionals/${p.id}`} className="text-sm font-medium text-primary-600 hover:underline">
                    {p.full_name} · {p.city}
                  </Link>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
}
