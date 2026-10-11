import { useEffect, useState } from 'react';
import api from '../services/api';

export default function AdminDashboard() {
  const [stats, setStats] = useState<any>(null);
  const [professionals, setProfessionals] = useState<any[]>([]);

  useEffect(() => {
    api.get('/admin/dashboard').then((r) => setStats(r.data)).catch(() => {});
    api.get('/admin/professionals').then((r) => setProfessionals(r.data.items || [])).catch(() => {});
  }, []);

  const verify = async (id: number, action: string) => {
    await api.post(`/admin/professionals/${id}/verify`, { action });
    setProfessionals((prev) =>
      prev.map((p) =>
        p.id === id
          ? { ...p, is_verified: action === 'approve', verification_status: action === 'approve' ? 'approved' : 'rejected' }
          : p
      )
    );
  };

  return (
    <div className="mx-auto max-w-6xl px-4 py-8 sm:px-6 lg:px-8">
      <h1 className="text-2xl font-bold">Admin Dashboard</h1>
      {stats && (
        <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {[
            ['Total Users', stats.total_users],
            ['Professionals', stats.total_professionals],
            ['Pending Verifications', stats.pending_verifications],
            ['Total Inquiries', stats.total_inquiries],
          ].map(([label, val]) => (
            <div key={label as string} className="card p-4 text-center">
              <div className="text-2xl font-bold text-primary-600">{val}</div>
              <div className="text-sm text-gray-500">{label}</div>
            </div>
          ))}
        </div>
      )}

      <div className="card mt-8 overflow-x-auto p-6">
        <h2 className="text-lg font-semibold">Professionals</h2>
        <table className="mt-4 w-full text-left text-sm">
          <thead>
            <tr className="border-b text-gray-500">
              <th className="pb-2 pr-4">Name</th>
              <th className="pb-2 pr-4">City</th>
              <th className="pb-2 pr-4">Verified</th>
              <th className="pb-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            {professionals.map((p) => (
              <tr key={p.id} className="border-b">
                <td className="py-3 pr-4 font-medium">{p.full_name}</td>
                <td className="py-3 pr-4">{p.city}</td>
                <td className="py-3 pr-4">{p.is_verified ? '✅' : '⏳'}</td>
                <td className="py-3 space-x-2">
                  {!p.is_verified && (
                    <button onClick={() => verify(p.id, 'approve')} className="text-xs font-medium text-green-600 hover:underline">
                      Approve
                    </button>
                  )}
                  <button onClick={() => verify(p.id, 'reject')} className="text-xs font-medium text-red-600 hover:underline">
                    Reject
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
