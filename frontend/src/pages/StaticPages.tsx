import { Link } from 'react-router-dom';

export function AboutPage() {
  return (
    <div className="mx-auto max-w-3xl px-4 py-12">
      <h1 className="text-3xl font-bold">About NirmanConnect</h1>
      <p className="mt-4 text-gray-600 leading-relaxed">
        NirmanConnect is an online marketplace that connects property owners, homeowners and builders with
        civil engineers, masons, electricians, plumbers, painters, carpenters and other skilled professionals
        across India.
      </p>
      <p className="mt-3 text-gray-600 leading-relaxed">
        Our core principle is direct contact. Customers discover and contact workers themselves.
        The platform does not automatically assign jobs. Pricing and project terms are agreed between
        the customer and the professional.
      </p>
    </div>
  );
}

export function ContactPage() {
  return (
    <div className="mx-auto max-w-3xl px-4 py-12">
      <h1 className="text-3xl font-bold">Contact Us</h1>
      <p className="mt-4 text-gray-600">For support, partnerships or feedback, email us at <a href="mailto:support@nirmanconnect.com" className="text-primary-600">support@nirmanconnect.com</a></p>
    </div>
  );
}

export function PrivacyPage() {
  return (
    <div className="mx-auto max-w-3xl px-4 py-12 prose">
      <h1 className="text-3xl font-bold">Privacy Policy</h1>
      <p className="mt-4 text-gray-600">We collect only the data necessary to operate the marketplace. Phone numbers are shown publicly only with explicit consent. Verification documents are accessible only to administrators. You may request account deletion at any time.</p>
    </div>
  );
}

export function TermsPage() {
  return (
    <div className="mx-auto max-w-3xl px-4 py-12">
      <h1 className="text-3xl font-bold">Terms & Conditions</h1>
      <p className="mt-4 text-gray-600">NirmanConnect is a discovery platform. We do not guarantee employment, worker availability, professional qualifications or work quality. Final pricing and project terms are agreed between the customer and the professional. Registration is free in the initial version.</p>
    </div>
  );
}

export function CategoriesPage() {
  return (
    <div className="mx-auto max-w-5xl px-4 py-12">
      <h1 className="text-3xl font-bold">Service Categories</h1>
      <p className="mt-2 text-gray-500">Browse all available trades</p>
      <div className="mt-8">
        <Link to="/professionals" className="btn-primary">Browse All Professionals</Link>
      </div>
    </div>
  );
}

export function NotFoundPage() {
  return (
    <div className="flex min-h-[50vh] flex-col items-center justify-center px-4">
      <h1 className="text-6xl font-bold text-primary-600">404</h1>
      <p className="mt-2 text-gray-500">Page not found</p>
      <Link to="/" className="btn-primary mt-6">Go Home</Link>
    </div>
  );
}
