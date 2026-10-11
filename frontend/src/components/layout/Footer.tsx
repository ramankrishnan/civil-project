import { Link } from 'react-router-dom';

export default function Footer() {
  return (
    <footer className="border-t border-gray-200 bg-gray-900 text-gray-300">
      <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="grid gap-8 md:grid-cols-4">
          <div>
            <div className="mb-3 flex items-center gap-2">
              <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary-600 text-sm font-bold text-white">
                N
              </span>
              <span className="text-lg font-bold text-white">NirmanConnect</span>
            </div>
            <p className="text-sm text-gray-400">
              Connect directly with trusted construction professionals and skilled workers near you.
            </p>
          </div>
          <div>
            <h4 className="mb-3 text-sm font-semibold text-white">For Customers</h4>
            <ul className="space-y-2 text-sm">
              <li><Link to="/professionals" className="hover:text-white">Find Professionals</Link></li>
              <li><Link to="/register?role=customer" className="hover:text-white">Register as Customer</Link></li>
              <li><Link to="/how-it-works" className="hover:text-white">How it Works</Link></li>
            </ul>
          </div>
          <div>
            <h4 className="mb-3 text-sm font-semibold text-white">For Professionals</h4>
            <ul className="space-y-2 text-sm">
              <li><Link to="/register?role=professional" className="hover:text-white">Register as Professional</Link></li>
              <li><Link to="/categories" className="hover:text-white">Service Categories</Link></li>
            </ul>
          </div>
          <div>
            <h4 className="mb-3 text-sm font-semibold text-white">Company</h4>
            <ul className="space-y-2 text-sm">
              <li><Link to="/about" className="hover:text-white">About Us</Link></li>
              <li><Link to="/contact" className="hover:text-white">Contact</Link></li>
              <li><Link to="/privacy" className="hover:text-white">Privacy Policy</Link></li>
              <li><Link to="/terms" className="hover:text-white">Terms & Conditions</Link></li>
            </ul>
          </div>
        </div>
        <div className="mt-10 border-t border-gray-800 pt-6 text-center text-sm text-gray-500">
          © {new Date().getFullYear()} NirmanConnect. Built for the Indian construction ecosystem.
        </div>
      </div>
    </footer>
  );
}
