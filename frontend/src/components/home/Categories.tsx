import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../../services/api';
import type { ServiceCategory } from '../../types';

export default function Categories() {
  const [categories, setCategories] = useState<ServiceCategory[]>([]);

  useEffect(() => {
    api.get('/categories').then((res) => setCategories(res.data.slice(0, 9))).catch(() => {});
  }, []);

  return (
    <section className="py-16">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <h2 className="text-3xl font-bold text-gray-900">Popular Categories</h2>
          <p className="mt-2 text-gray-600">Browse skilled professionals by trade</p>
        </div>
        <div className="mt-10 grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-3">
          {categories.map((cat) => (
            <Link
              key={cat.id}
              to={`/professionals?category=${cat.slug}`}
              className="card flex flex-col items-center gap-3 p-6 transition hover:border-primary-300 hover:shadow-md"
            >
              <span className="text-4xl">{cat.icon || '🔧'}</span>
              <span className="text-center text-sm font-semibold text-gray-800">{cat.name}</span>
            </Link>
          ))}
        </div>
        <div className="mt-8 text-center">
          <Link to="/categories" className="text-sm font-semibold text-primary-600 hover:text-primary-700">
            View all categories →
          </Link>
        </div>
      </div>
    </section>
  );
}
