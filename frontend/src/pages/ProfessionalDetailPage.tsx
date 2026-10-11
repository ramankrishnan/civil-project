import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { MapPin, Star, BadgeCheck, Phone, MessageCircle, Briefcase, Clock } from 'lucide-react';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';
import type { ProfessionalProfile } from '../types';

export default function ProfessionalDetailPage() {
  const { id } = useParams();
  const { user } = useAuth();
  const [prof, setProf] = useState<ProfessionalProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [inquiryOpen, setInquiryOpen] = useState(false);
  const [inquiryForm, setInquiryForm] = useState({ work_description: '', location: '', approximate_budget: '' });
  const [sending, setSending] = useState(false);
  const [msg, setMsg] = useState('');

  useEffect(() => {
    api.get(`/professionals/${id}`).then((r) => setProf(r.data)).catch(() => {}).finally(() => setLoading(false));
  }, [id]);

  const sendInquiry = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!user) {
      setMsg('Please login as a customer to send an inquiry.');
      return;
    }
    setSending(true);
    try {
      await api.post('/inquiries', {
        professional_id: Number(id),
        work_description: inquiryForm.work_description,
        location: inquiryForm.location,
        approximate_budget: inquiryForm.approximate_budget || null,
      });
      setMsg('Inquiry sent successfully!');
      setInquiryOpen(false);
    } catch (err: any) {
      setMsg(err.response?.data?.error || 'Failed to send inquiry');
    } finally {
      setSending(false);
    }
  };

  if (loading) return <div className="flex justify-center py-20"><div className="h-8 w-8 animate-spin rounded-full border-4 border-primary-600 border-t-transparent" /></div>;
  if (!prof) return <div className="py-20 text-center text-gray-500">Professional not found</div>;

  return (
    <div className="mx-auto max-w-5xl px-4 py-8 sm:px-6 lg:px-8">
      <div className="card overflow-hidden">
        <div className="bg-gradient-to-r from-primary-600 to-primary-700 px-6 py-8 text-white sm:px-8">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center">
            <div className="flex h-20 w-20 items-center justify-center rounded-full bg-white/20 text-3xl font-bold">
              {prof.full_name.charAt(0)}
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-2xl font-bold">{prof.full_name}</h1>
                {prof.is_verified && <BadgeCheck className="h-6 w-6" />}
              </div>
              <p className="text-primary-100">{prof.skills?.[0]?.category_name || 'Professional'}</p>
              <div className="mt-1 flex items-center gap-1 text-sm text-primary-100">
                <MapPin className="h-4 w-4" />
                {prof.locality ? `${prof.locality}, ` : ''}{prof.city}
                {prof.pin_code && ` · ${prof.pin_code}`}
              </div>
            </div>
          </div>
        </div>

        <div className="grid gap-8 p-6 sm:p-8 lg:grid-cols-3">
          <div className="lg:col-span-2 space-y-6">
            {prof.introduction && (
              <div>
                <h2 className="text-lg font-semibold">About</h2>
                <p className="mt-2 text-gray-600 whitespace-pre-line">{prof.introduction}</p>
              </div>
            )}
            {prof.service_description && (
              <div>
                <h2 className="text-lg font-semibold">Services</h2>
                <p className="mt-2 text-gray-600 whitespace-pre-line">{prof.service_description}</p>
              </div>
            )}
            {prof.skills?.length > 0 && (
              <div>
                <h2 className="text-lg font-semibold">Skills</h2>
                <div className="mt-2 flex flex-wrap gap-2">
                  {prof.skills.map((s) => (
                    <span key={s.id} className="rounded-full bg-primary-50 px-3 py-1 text-sm font-medium text-primary-700">
                      {s.category_name}
                    </span>
                  ))}
                </div>
              </div>
            )}
            {prof.portfolio_items?.length > 0 && (
              <div>
                <h2 className="text-lg font-semibold">Portfolio</h2>
                <div className="mt-3 grid grid-cols-2 gap-3 sm:grid-cols-3">
                  {prof.portfolio_items.map((item) => (
                    <div key={item.id} className="aspect-square overflow-hidden rounded-lg bg-gray-100">
                      <img src={item.image_url} alt={item.title || ''} className="h-full w-full object-cover" />
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          <div className="space-y-4">
            <div className="card p-4 space-y-3">
              <div className="flex items-center gap-2 text-sm">
                <Briefcase className="h-4 w-4 text-gray-400" />
                <span>{prof.years_of_experience}+ years experience</span>
              </div>
              <div className="flex items-center gap-2 text-sm">
                <Clock className="h-4 w-4 text-gray-400" />
                <span className="capitalize">{prof.availability.replace('_', ' ')}</span>
              </div>
              {prof.price_amount && (
                <div className="text-lg font-bold text-primary-600">
                  ₹{prof.price_amount}
                  <span className="text-sm font-normal text-gray-500">
                    /{prof.pricing_type === 'daily' ? 'day' : prof.pricing_type === 'hourly' ? 'hr' : prof.pricing_type === 'per_sqft' ? 'sq.ft' : 'project'}
                  </span>
                </div>
              )}
              {prof.average_rating && (
                <div className="flex items-center gap-1 text-amber-600">
                  <Star className="h-4 w-4 fill-current" />
                  <span className="font-semibold">{prof.average_rating}</span>
                  <span className="text-sm text-gray-500">({prof.review_count} reviews)</span>
                </div>
              )}
            </div>

            <div className="space-y-2">
              {prof.phone && (
                <a href={`tel:${prof.phone}`} className="btn-primary w-full">
                  <Phone className="h-4 w-4" /> Call Now
                </a>
              )}
              {prof.whatsapp && (
                <a
                  href={`https://wa.me/91${prof.whatsapp.replace(/\D/g, '')}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn-secondary w-full"
                >
                  <MessageCircle className="h-4 w-4" /> WhatsApp
                </a>
              )}
              <button onClick={() => setInquiryOpen(true)} className="btn-accent w-full">
                Send Project Inquiry
              </button>
            </div>

            {msg && <p className="text-sm text-center text-primary-600">{msg}</p>}
          </div>
        </div>
      </div>

      {inquiryOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
          <div className="card w-full max-w-md p-6">
            <h3 className="text-lg font-semibold">Send Project Inquiry</h3>
            <form onSubmit={sendInquiry} className="mt-4 space-y-3">
              <textarea
                className="input-field"
                rows={4}
                placeholder="Describe the work you need..."
                required
                value={inquiryForm.work_description}
                onChange={(e) => setInquiryForm({ ...inquiryForm, work_description: e.target.value })}
              />
              <input
                className="input-field"
                placeholder="Location (optional)"
                value={inquiryForm.location}
                onChange={(e) => setInquiryForm({ ...inquiryForm, location: e.target.value })}
              />
              <input
                className="input-field"
                type="number"
                placeholder="Approx. budget in ₹ (optional)"
                value={inquiryForm.approximate_budget}
                onChange={(e) => setInquiryForm({ ...inquiryForm, approximate_budget: e.target.value })}
              />
              <div className="flex gap-2">
                <button type="button" onClick={() => setInquiryOpen(false)} className="btn-secondary flex-1">
                  Cancel
                </button>
                <button type="submit" disabled={sending} className="btn-primary flex-1">
                  {sending ? 'Sending...' : 'Send Inquiry'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
