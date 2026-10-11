import { Link, useNavigate } from 'react-router-dom';
import { useState } from 'react';
import { Menu, X, User, LogOut, LayoutDashboard, Heart } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [open, setOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const dashboardPath =
    user?.role === 'admin'
      ? '/admin'
      : user?.role === 'professional'
      ? '/dashboard/professional'
      : '/dashboard/customer';

  return (
    <header className="sticky top-0 z-50 border-b border-gray-200 bg-white/95 backdrop-blur">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 sm:px-6 lg:px-8">
        <Link to="/" className="flex items-center gap-2">
          <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-primary-600 text-lg font-bold text-white">
            N
          </span>
          <span className="text-xl font-bold text-gray-900">
            Nirman<span className="text-primary-600">Connect</span>
          </span>
        </Link>

        <nav className="hidden items-center gap-6 md:flex">
          <Link to="/professionals" className="text-sm font-medium text-gray-600 hover:text-primary-600">
            Find Professionals
          </Link>
          <Link to="/categories" className="text-sm font-medium text-gray-600 hover:text-primary-600">
            Categories
          </Link>
          <Link to="/about" className="text-sm font-medium text-gray-600 hover:text-primary-600">
            About
          </Link>
        </nav>

        <div className="hidden items-center gap-3 md:flex">
          {user ? (
            <>
              <Link to={dashboardPath} className="btn-secondary text-sm">
                <LayoutDashboard className="h-4 w-4" />
                Dashboard
              </Link>
              <button onClick={handleLogout} className="btn-secondary text-sm">
                <LogOut className="h-4 w-4" />
                Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="btn-secondary text-sm">
                Login
              </Link>
              <Link to="/register" className="btn-primary text-sm">
                Register
              </Link>
            </>
          )}
        </div>

        <button className="md:hidden" onClick={() => setOpen(!open)} aria-label="Toggle menu">
          {open ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
        </button>
      </div>

      {open && (
        <div className="border-t border-gray-100 bg-white px-4 py-4 md:hidden">
          <div className="flex flex-col gap-3">
            <Link to="/professionals" onClick={() => setOpen(false)} className="text-sm font-medium">
              Find Professionals
            </Link>
            <Link to="/categories" onClick={() => setOpen(false)} className="text-sm font-medium">
              Categories
            </Link>
            {user ? (
              <>
                <Link to={dashboardPath} onClick={() => setOpen(false)} className="text-sm font-medium">
                  Dashboard
                </Link>
                <button onClick={handleLogout} className="text-left text-sm font-medium text-red-600">
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link to="/login" onClick={() => setOpen(false)} className="btn-secondary text-sm">
                  Login
                </Link>
                <Link to="/register" onClick={() => setOpen(false)} className="btn-primary text-sm">
                  Register
                </Link>
              </>
            )}
          </div>
        </div>
      )}
    </header>
  );
}
