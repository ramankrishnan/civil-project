import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import type { ProjectInquiry, ProfessionalProfile } from '../types';

export default function ProfessionalDashboard() {
  const { user, refreshUser } = useAuth();
  const [inquiries, setInquiries] = useState<ProjectInquiry[]>([]);
  const [profile, setProfile] = useState<ProfessionalProfile | null>(null);

  useEffect(() => {
    api.get('/inquiries').then((r) => setInquiries(r.data)).catch(() => {});
    api.get('/professionals/me').then((r) => setProfile(r.data)).catch(() => {});
  }, []);

  return (
    <div className="mx-auto max-w-5xl px-4 py-8 sm:px-6 lg:px-8">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold">Professional Dashboard</h1>
          <p className="text-gray-500">Welcome, {profile?.full_name || user?.email}</p>
        </div>
        <Link to="/dashboard/professional/edit" className="btn-primary text-sm">Edit Profile</Link>
      </div>

      {profile && (
        <div className="mt-6 grid gap-4 sm:grid-cols-3">
          <div className="card p-4 text-center">
            <div className="text-2xl font-bold text-primary-600">{profile.profile_visits || 0}</div>
            <div className="text-sm text-gray-500">Profile Visits</div>
          </div>
          <div className="card p-4 text-center">
            <div className="text-2xl font-bold text-primary-600">{inquiries.length}</div>
            <div className="text-sm text-gray-500">Total Inquiries</div>
          </div>
          <div className="card p-4 text-center">
            <div className="text-2xl font-bold text-primary-600 capitalize">{profile.availability.replace('_', ' ')}</div>
            <div className="text-sm text-gray-500">Availability</div>
          </div>
        </div>
      )}

      <div className="card mt-8 p-6">
        <h2 className="text-lg font-semibold">Recent Inquiries</h2>
        {inquiries.length === 0 ? (
          <p className="mt-4 text-sm text-gray-500">No inquiries yet. Keep your profile updated to attract customers.</p>
        ) : (
          <ul className="mt-4 space-y-3">
            {inquiries.map((i) => (
              <li key={i.id} className="flex flex-wrap items-center justify-between gap-2 rounded-lg border p-3 text-sm">
                <div>
                  <div className="font-medium">{i.customer_name}</div>
                  <div className="text-gray-500">{i.work_description}</div>
                  {i.approximate_budget && <div className="text-xs text-gray-400">Budget: ₹{i.approximate_budget}</div>}
                </div>
                <select
                  className="input-field w-auto text-xs"
                  value={i.status}
                  onChange={async (e) => {
                    await api.patch(`/inquiries/${i.id}/status`, { status: e.target.value });
                    setInquiries((prev) => prev.map((x) => (x.id === i.id ? { ...x, status: e.target.value } : x)));
                  }}
                >
                  {['new', 'contacted', 'discussing', 'accepted', 'completed', 'cancelled'].map((s) => (
                    <option key={s} value={s}>{s}</option>
                  ))}
                </select>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
