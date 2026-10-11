import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { MapPin, Star, BadgeCheck } from 'lucide-react';
import api from '../../services/api';
import type { ProfessionalProfile } from '../../types';

export default function FeaturedProfessionals() {
  const [items, setItems] = useState<ProfessionalProfile[]>([]);

  useEffect(() => {
    api.get('/professionals/featured').then((res) => setItems(res.data)).catch(() => {});
  }, []);

  if (items.length === 0) return null;

  return (
    <section className="py-16">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex items-end justify-between">
          <div>
            <h2 className="text-3xl font-bold text-gray-900">Featured Professionals</h2>
            <p className="mt-1 text-gray-600">Verified and highly visited profiles</p>
          </div>
          <Link to="/professionals" className="hidden text-sm font-semibold text-primary-600 hover:text-primary-700 sm:block">
            View all →
          </Link>
        </div>
        <div className="mt-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {items.map((p) => (
            <Link key={p.id} to={`/professionals/${p.id}`} className="card overflow-hidden transition hover:shadow-md">
              <div className="flex h-32 items-center justify-center bg-gradient-to-br from-primary-50 to-primary-100">
                {p.profile_photo ? (
                  <img src={p.profile_photo} alt={p.full_name} className="h-full w-full object-cover" />
                ) : (
                  <span className="text-4xl font-bold text-primary-300">
                    {p.full_name.charAt(0)}
                  </span>
                )}
              </div>
              <div className="p-4">
                <div className="flex items-center gap-1">
                  <h3 className="font-semibold text-gray-900">{p.full_name}</h3>
                  {p.is_verified && <BadgeCheck className="h-4 w-4 text-primary-600" />}
                </div>
                <p className="mt-0.5 text-sm text-gray-500">
                  {p.skills?.[0]?.category_name || 'Professional'}
                </p>
                <div className="mt-2 flex items-center gap-1 text-xs text-gray-500">
                  <MapPin className="h-3.5 w-3.5" />
                  {p.locality ? `${p.locality}, ` : ''}{p.city}
                </div>
                <div className="mt-2 flex items-center justify-between text-sm">
                  <span className="text-gray-600">{p.years_of_experience}+ yrs exp</span>
                  {p.average_rating && (
                    <span className="flex items-center gap-0.5 text-amber-600">
                      <Star className="h-3.5 w-3.5 fill-current" />
                      {p.average_rating}
                    </span>
                  )}
                </div>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </section>
  );
}
