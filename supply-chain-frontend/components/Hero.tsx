export default function Hero() {
  return (
    <section className="bg-gray-50 pt-32 pb-24">
      <div className="mx-auto grid max-w-6xl items-center gap-12 px-6 md:grid-cols-[minmax(0,1fr)_minmax(0,1.1fr)]">
        <div className="flex flex-col gap-6">
          <span className="text-sm font-semibold uppercase tracking-[0.3em] text-indigo-600">
            Analytics for the web
          </span>
          <h1 className="text-5xl font-semibold leading-tight text-gray-900 md:text-6xl">
            Supa-Fast & Supa-Reliable insight into your traffic
          </h1>
          <p className="text-lg text-gray-600 md:max-w-xl">
            Woyage is a free, open-source analytics platform that keeps you close to what
            matters: real-time visitor behavior, performance metrics, and privacy-first
            reporting without the complexity.
          </p>
          <div className="flex flex-col gap-4 sm:flex-row">
            <a
              id="get-started"
              href="#steps"
              className="rounded-full bg-gray-900 px-6 py-3 text-center text-sm font-semibold text-white transition hover:bg-gray-700"
            >
              Get Started
            </a>
            <a
              href="#features"
              className="rounded-full border border-gray-300 px-6 py-3 text-center text-sm font-semibold text-gray-900 transition hover:border-gray-900 hover:text-gray-900"
            >
              View Features
            </a>
          </div>
          <div className="flex flex-wrap gap-4 text-sm text-gray-500">
            <div className="flex items-center gap-2">
              <span className="inline-flex h-2 w-2 rounded-full bg-emerald-500" />
              Privacy-first tracking
            </div>
            <div className="flex items-center gap-2">
              <span className="inline-flex h-2 w-2 rounded-full bg-indigo-500" />
              Instant dashboards
            </div>
            <div className="flex items-center gap-2">
              <span className="inline-flex h-2 w-2 rounded-full bg-amber-500" />
              No usage limits
            </div>
          </div>
        </div>
        <div className="rounded-3xl border border-gray-200 bg-white p-4 shadow-xl shadow-indigo-100/20">
          <img
            src="https://www.woyage.app/screenshots/dashboard-screenshot.png"
            alt="Woyage analytics dashboard"
            className="w-full rounded-2xl"
          />
        </div>
      </div>
    </section>
  );
}
