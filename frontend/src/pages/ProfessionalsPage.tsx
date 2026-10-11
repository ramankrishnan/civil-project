import { useEffect, useState } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { MapPin, Star, BadgeCheck, Phone, Filter } from 'lucide-react';
import api from '../services/api';
import type { ProfessionalProfile, ServiceCategory, PaginatedResponse } from '../types';

export default function ProfessionalsPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [data, setData] = useState<PaginatedResponse<ProfessionalProfile> | null>(null);
  const [categories, setCategories] = useState<ServiceCategory[]>([]);
  const [loading, setLoading] = useState(true);
  const [showFilters, setShowFilters] = useState(false);

  const q = searchParams.get('q') || '';
  const city = searchParams.get('city') || '';
  const category = searchParams.get('category') || '';
  const page = Number(searchParams.get('page') || 1);
  const sort = searchParams.get('sort') || 'relevance';
  const verified = searchParams.get('verified') || '';

  useEffect(() => {
    api.get('/categories').then((r) => setCategories(r.data)).catch(() => {});
  }, []);

  useEffect(() => {
    setLoading(true);
    const params: Record<string, string | number> = { page, sort };
    if (q) params.q = q;
    if (city) params.city = city;
    if (category) params.category = category;
    if (verified) params.verified = verified;
    api
      .get('/professionals', { params })
      .then((r) => setData(r.data))
      .catch(() => setData(null))
      .finally(() => setLoading(false));
  }, [q, city, category, page, sort, verified]);

  const updateParam = (key: string, value: string) => {
    const next = new URLSearchParams(searchParams);
    if (value) next.set(key, value);
    else next.delete(key);
    if (key !== 'page') next.delete('page');
    setSearchParams(next);
  };

  return (
    <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
      <div className="mb-6 flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Browse Professionals</h1>
          <p className="text-sm text-gray-500">
            {data ? `${data.total} professionals found` : 'Searching...'}
          </p>
        </div>
        <button onClick={() => setShowFilters(!showFilters)} className="btn-secondary text-sm lg:hidden">
          <Filter className="h-4 w-4" /> Filters
        </button>
      </div>

      <div className="flex gap-8">
        {/* Filters sidebar */}
        <aside className={`w-64 shrink-0 space-y-6 ${showFilters ? 'block' : 'hidden'} lg:block`}>
          <div className="card p-4">
            <h3 className="mb-3 text-sm font-semibold">Search</h3>
            <input
              className="input-field mb-2"
              placeholder="Name or skill..."
              defaultValue={q}
              onKeyDown={(e) => e.key === 'Enter' && updateParam('q', (e.target as HTMLInputElement).value)}
            />
            <input
              className="input-field"
              placeholder="City..."
              defaultValue={city}
              onKeyDown={(e) => e.key === 'Enter' && updateParam('city', (e.target as HTMLInputElement).value)}
            />
          </div>
          <div className="card p-4">
            <h3 className="mb-3 text-sm font-semibold">Category</h3>
            <select
              className="input-field"
              value={category}
              onChange={(e) => updateParam('category', e.target.value)}
            >
              <option value="">All categories</option>
              {categories.map((c) => (
                <option key={c.id} value={c.slug}>{c.name}</option>
              ))}
            </select>
          </div>
          <div className="card p-4">
            <h3 className="mb-3 text-sm font-semibold">Sort by</h3>
            <select className="input-field" value={sort} onChange={(e) => updateParam('sort', e.target.value)}>
              <option value="relevance">Relevance</option>
              <option value="experience">Experience</option>
              <option value="newest">Newest</option>
            </select>
          </div>
          <div className="card p-4">
            <label className="flex items-center gap-2 text-sm">
              <input
                type="checkbox"
                checked={verified === 'true'}
                onChange={(e) => updateParam('verified', e.target.checked ? 'true' : '')}
              />
              Verified only
            </label>
          </div>
        </aside>

        {/* Results */}
        <div className="flex-1">
          {loading ? (
            <div className="grid gap-4 sm:grid-cols-2">
              {[...Array(6)].map((_, i) => (
                <div key={i} className="card h-40 animate-pulse bg-gray-100" />
              ))}
            </div>
          ) : !data || data.items.length === 0 ? (
            <div className="card p-12 text-center">
              <p className="text-gray-500">No professionals found. Try adjusting your filters.</p>
            </div>
          ) : (
            <>
              <div className="grid gap-4 sm:grid-cols-2">
                {data.items.map((p) => (
                  <div key={p.id} className="card flex gap-4 p-4 transition hover:shadow-md">
                    <div className="flex h-16 w-16 shrink-0 items-center justify-center rounded-full bg-primary-100 text-xl font-bold text-primary-600">
                      {p.profile_photo ? (
                        <img src={p.profile_photo} alt="" className="h-full w-full rounded-full object-cover" />
                      ) : (
                        p.full_name.charAt(0)
                      )}
                    </div>
                    <div className="min-w-0 flex-1">
                      <div className="flex items-center gap-1">
                        <Link to={`/professionals/${p.id}`} className="font-semibold text-gray-900 hover:text-primary-600">
                          {p.full_name}
                        </Link>
                        {p.is_verified && <BadgeCheck className="h-4 w-4 text-primary-600" />}
                      </div>
                      <p className="text-sm text-gray-500">{p.skills?.[0]?.category_name || 'Professional'}</p>
                      <div className="mt-1 flex items-center gap-1 text-xs text-gray-500">
                        <MapPin className="h-3 w-3" />
                        {p.locality ? `${p.locality}, ` : ''}{p.city}
                      </div>
                      <div className="mt-2 flex flex-wrap items-center gap-3 text-sm">
                        <span>{p.years_of_experience}+ yrs</span>
                        {p.price_amount && (
                          <span className="text-primary-600 font-medium">
                            ₹{p.price_amount}/{p.pricing_type === 'daily' ? 'day' : p.pricing_type === 'hourly' ? 'hr' : p.pricing_type}
                          </span>
                        )}
                        {p.average_rating && (
                          <span className="flex items-center gap-0.5 text-amber-600">
                            <Star className="h-3.5 w-3.5 fill-current" /> {p.average_rating}
                          </span>
                        )}
                      </div>
                      <div className="mt-3 flex gap-2">
                        <Link to={`/professionals/${p.id}`} className="btn-primary text-xs px-3 py-1.5">
                          View Profile
                        </Link>
                        {p.phone && (
                          <a href={`tel:${p.phone}`} className="btn-secondary text-xs px-3 py-1.5">
                            <Phone className="h-3.5 w-3.5" /> Call
                          </a>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
              {data.pages > 1 && (
                <div className="mt-8 flex justify-center gap-2">
                  {Array.from({ length: data.pages }, (_, i) => i + 1).map((p) => (
                    <button
                      key={p}
                      onClick={() => updateParam('page', String(p))}
                      className={`rounded-lg px-3 py-1.5 text-sm font-medium ${
                        p === data.page ? 'bg-primary-600 text-white' : 'bg-white text-gray-700 border'
                      }`}
                    >
                      {p}
                    </button>
                  ))}
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}
