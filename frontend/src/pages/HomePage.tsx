import Hero from '../components/home/Hero';
import Categories from '../components/home/Categories';
import HowItWorks from '../components/home/HowItWorks';
import FeaturedProfessionals from '../components/home/FeaturedProfessionals';

export default function HomePage() {
  return (
    <>
      <Hero />
      <Categories />
      <HowItWorks />
      <FeaturedProfessionals />
      <section className="bg-primary-700 py-16 text-white">
        <div className="mx-auto max-w-3xl px-4 text-center">
          <h2 className="text-3xl font-bold">Ready to get started?</h2>
          <p className="mt-2 text-primary-100">
            Whether you need a skilled worker or want to grow your client base — NirmanConnect is for you.
          </p>
          <div className="mt-8 flex flex-wrap justify-center gap-4">
            <a href="/professionals" className="rounded-lg bg-white px-6 py-3 text-sm font-semibold text-primary-700 hover:bg-primary-50">
              Find a Professional
            </a>
            <a href="/register?role=professional" className="rounded-lg border border-white/40 px-6 py-3 text-sm font-semibold hover:bg-white/10">
              Join as Professional
            </a>
          </div>
        </div>
      </section>
    </>
  );
}
