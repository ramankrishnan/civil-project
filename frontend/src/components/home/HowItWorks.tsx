import { Search, Users, Phone, Handshake } from 'lucide-react';

const steps = [
  {
    icon: Search,
    title: 'Search for a skill',
    desc: 'Enter the service you need and your location to find nearby professionals.',
  },
  {
    icon: Users,
    title: 'Compare profiles',
    desc: 'View experience, skills, pricing and work samples to shortlist the right fit.',
  },
  {
    icon: Phone,
    title: 'Contact directly',
    desc: 'Call or message the professional on WhatsApp. No middleman required.',
  },
  {
    icon: Handshake,
    title: 'Agree on terms',
    desc: 'Discuss the work, negotiate pricing and finalise the project between yourselves.',
  },
];

export default function HowItWorks() {
  return (
    <section className="bg-white py-16">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <h2 className="text-3xl font-bold text-gray-900">How it Works</h2>
          <p className="mt-2 text-gray-600">Simple, transparent and direct</p>
        </div>
        <div className="mt-12 grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
          {steps.map((step, i) => (
            <div key={i} className="relative text-center">
              <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-primary-100 text-primary-600">
                <step.icon className="h-7 w-7" />
              </div>
              <div className="mt-1 text-xs font-bold text-primary-500">STEP {i + 1}</div>
              <h3 className="mt-2 text-lg font-semibold text-gray-900">{step.title}</h3>
              <p className="mt-1 text-sm text-gray-600">{step.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
