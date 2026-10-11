import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search } from 'lucide-react';

export default function Hero() {
  const navigate = useNavigate();
  const [service, setService] = useState('');
  const [location, setLocation] = useState('');

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    const params = new URLSearchParams();
    if (service) params.set('q', service);
    if (location) params.set('city', location);
    navigate(`/professionals?${params.toString()}`);
  };

  return (
    <section className="relative overflow-hidden bg-gradient-to-br from-primary-700 via-primary-600 to-primary-800 text-white">
      <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxnIGZpbGw9IiNmZmYiIGZpbGwtb3BhY2l0eT0iMC4wNSI+PHBhdGggZD0iTTM2IDM0djItSDI0di0yaDEyek0zNiAyNHYySDI0di0yaDEyeiIvPjwvZz48L2c+PC9zdmc+')] opacity-40" />
      <div className="relative mx-auto max-w-7xl px-4 py-20 sm:px-6 sm:py-28 lg:px-8">
        <div className="mx-auto max-w-3xl text-center">
          <h1 className="text-4xl font-extrabold tracking-tight sm:text-5xl lg:text-6xl">
            Find the Right Professional for Your Next Project
          </h1>
          <p className="mt-4 text-lg text-primary-100 sm:text-xl">
            Connect directly with trusted construction professionals and skilled workers near you.
          </p>

          <form onSubmit={handleSearch} className="mt-10 rounded-2xl bg-white p-2 shadow-xl sm:flex sm:items-center sm:gap-2">
            <div className="flex flex-1 items-center gap-2 rounded-xl px-3 py-2">
              <Search className="h-5 w-5 text-gray-400" />
              <input
                type="text"
                placeholder="What service do you need?"
                value={service}
                onChange={(e) => setService(e.target.value)}
                className="w-full border-0 bg-transparent text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-0"
              />
            </div>
            <div className="my-2 h-px bg-gray-200 sm:my-0 sm:h-8 sm:w-px" />
            <div className="flex flex-1 items-center gap-2 rounded-xl px-3 py-2">
              <input
                type="text"
                placeholder="City, locality or PIN code"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                className="w-full border-0 bg-transparent text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-0"
              />
            </div>
            <button type="submit" className="w-full rounded-xl bg-primary-600 px-6 py-3 text-sm font-semibold text-white hover:bg-primary-700 sm:w-auto">
              Search Professionals
            </button>
          </form>

          <div className="mt-8 flex flex-wrap justify-center gap-4">
            <button
              onClick={() => navigate('/professionals')}
              className="rounded-lg border border-white/30 bg-white/10 px-6 py-2.5 text-sm font-semibold backdrop-blur hover:bg-white/20"
            >
              Find a Professional
            </button>
            <button
              onClick={() => navigate('/register?role=professional')}
              className="rounded-lg bg-accent-500 px-6 py-2.5 text-sm font-semibold text-white hover:bg-accent-600"
            >
              Register as a Professional
            </button>
          </div>
        </div>
      </div>
    </section>
  );
}
