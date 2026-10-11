import { useState } from 'react';
import { Link, useNavigate, useSearchParams } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function RegisterPage() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const defaultRole = (searchParams.get('role') as 'customer' | 'professional') || 'customer';

  const [form, setForm] = useState({
    email: '',
    password: '',
    full_name: '',
    phone: '',
    city: '',
    locality: '',
    pin_code: '',
    role: defaultRole,
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await register(form);
      navigate(form.role === 'professional' ? '/dashboard/professional' : '/dashboard/customer');
    } catch (err: any) {
      setError(err.response?.data?.error || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-[70vh] items-center justify-center px-4 py-12">
      <div className="card w-full max-w-lg p-8">
        <h1 className="text-2xl font-bold text-center">Create your account</h1>
        <p className="mt-1 text-center text-sm text-gray-500">Join NirmanConnect free</p>

        <div className="mt-4 flex rounded-lg border p-1">
          <button
            type="button"
            onClick={() => setForm({ ...form, role: 'customer' })}
            className={`flex-1 rounded-md py-2 text-sm font-medium ${form.role === 'customer' ? 'bg-primary-600 text-white' : 'text-gray-600'}`}
          >
            I'm a Customer
          </button>
          <button
            type="button"
            onClick={() => setForm({ ...form, role: 'professional' })}
            className={`flex-1 rounded-md py-2 text-sm font-medium ${form.role === 'professional' ? 'bg-primary-600 text-white' : 'text-gray-600'}`}
          >
            I'm a Professional
          </button>
        </div>

        <form onSubmit={handleSubmit} className="mt-6 space-y-3">
          {error && <div className="rounded-lg bg-red-50 px-4 py-2 text-sm text-red-600">{error}</div>}
          <input className="input-field" placeholder="Full name *" required value={form.full_name} onChange={(e) => setForm({ ...form, full_name: e.target.value })} />
          <input className="input-field" type="email" placeholder="Email *" required value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} />
          <input className="input-field" type="password" placeholder="Password (min 8 chars) *" required minLength={8} value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} />
          <input className="input-field" placeholder="Phone number" value={form.phone} onChange={(e) => setForm({ ...form, phone: e.target.value })} />
          <div className="grid grid-cols-2 gap-3">
            <input className="input-field" placeholder={form.role === 'professional' ? 'City *' : 'City'} required={form.role === 'professional'} value={form.city} onChange={(e) => setForm({ ...form, city: e.target.value })} />
            <input className="input-field" placeholder="Locality" value={form.locality} onChange={(e) => setForm({ ...form, locality: e.target.value })} />
          </div>
          <input className="input-field" placeholder="PIN code" value={form.pin_code} onChange={(e) => setForm({ ...form, pin_code: e.target.value })} />
          <button type="submit" disabled={loading} className="btn-primary w-full">
            {loading ? 'Creating account...' : 'Register'}
          </button>
        </form>
        <p className="mt-4 text-center text-sm text-gray-500">
          Already have an account? <Link to="/login" className="font-semibold text-primary-600">Login</Link>
        </p>
      </div>
    </div>
  );
}
