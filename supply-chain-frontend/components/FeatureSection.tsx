const featureCards = [
  {
    title: "Real-time visitor insights",
    description: "See live sessions, top pages, and retention without switching tabs.",
  },
  {
    title: "Global reach visualized",
    description: "Heatmaps show where your visitors come from across the world.",
  },
  {
    title: "Language breakdown",
    description: "Understand the languages your audience speaks for localized content.",
  },
  {
    title: "Live activity feed",
    description: "Follow page views, conversions, and funnels as they happen.",
  },
  {
    title: "Source attribution",
    description: "Track referral, direct, and search traffic with clean attribution.",
  },
  {
    title: "Device analytics",
    description: "Break down usage by device, browser, and operating system.",
  },
];

const steps = [
  {
    number: "01",
    title: "Add your first site",
    description: "Open the dashboard, click Add Site, and drop in your domain to start tracking.",
  },
  {
    number: "02",
    title: "Install the tracking pixel",
    description: "Place the lightweight script tag inside the head of your site or through your tag manager.",
  },
  {
    number: "03",
    title: "Watch data flow",
    description: "Refresh your dashboard to see visitors, sources, and events in real-time.",
  },
];

const stack = ["Next.js", "Tailwind CSS", "PlanetScale", "ClickHouse", "Edge Functions", "TypeScript"];

const faqs = [
  {
    question: "Is Woyage really free?",
    answer: "Yes. Woyage is fully open-source and free to self-host or use on our hosted cloud.",
  },
  {
    question: "How lightweight is the script?",
    answer: "The tracking script is under 1kb gzipped, ships with no cookies, and loads on the edge.",
  },
  {
    question: "Can I export my data?",
    answer: "You can export raw events, dashboards, and reports as CSV or stream them to your warehouse.",
  },
];

export default function FeatureSection() {
  return (
    <div className="bg-white">
      <section id="features" className="py-24">
        <div className="mx-auto max-w-6xl px-6">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-4xl font-semibold text-gray-900 md:text-5xl">Woyage is packed with features</h2>
            <p className="mt-6 text-lg text-gray-600">
              An overview of everything you need to track performance, understand audiences, and act on live data.
            </p>
          </div>
          <div className="mt-16 grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {featureCards.map((feature) => (
              <div
                key={feature.title}
                className="flex h-full flex-col gap-4 rounded-3xl border border-gray-200 bg-white p-8 text-left shadow-sm transition hover:-translate-y-1 hover:shadow-lg"
              >
                <h3 className="text-xl font-semibold text-gray-900">{feature.title}</h3>
                <p className="text-sm text-gray-600">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section id="steps" className="border-t border-gray-200 bg-gray-50 py-24">
        <div className="mx-auto max-w-6xl px-6">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-4xl font-semibold text-gray-900 md:text-5xl">Get Started in 3 Simple Steps</h2>
            <p className="mt-6 text-lg text-gray-600">
              Go from sign-up to live dashboards in minutes with a setup flow focused on speed.
            </p>
          </div>
          <div className="mt-16 grid gap-6 md:grid-cols-3">
            {steps.map((step) => (
              <div key={step.number} className="rounded-3xl bg-white p-8 shadow-sm">
                <span className="text-sm font-semibold uppercase tracking-[0.4em] text-indigo-500">{step.number}</span>
                <h3 className="mt-4 text-xl font-semibold text-gray-900">{step.title}</h3>
                <p className="mt-4 text-sm text-gray-600">{step.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section id="stack" className="border-t border-gray-200 py-24">
        <div className="mx-auto max-w-6xl px-6">
          <div className="grid gap-12 lg:grid-cols-[minmax(0,1.2fr)_minmax(0,1fr)]">
            <div>
              <h2 className="text-4xl font-semibold text-gray-900 md:text-5xl">Open-source and built to perform</h2>
              <p className="mt-6 text-lg text-gray-600">
                Powered by modern infrastructure that keeps dashboards blazing fast, reliable, and private by design.
              </p>
            </div>
            <div className="flex flex-wrap gap-3">
              {stack.map((item) => (
                <span
                  key={item}
                  className="rounded-full border border-gray-200 bg-gray-50 px-5 py-2 text-sm font-semibold text-gray-800"
                >
                  {item}
                </span>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section id="faq" className="border-t border-gray-200 bg-gray-50 py-24">
        <div className="mx-auto max-w-6xl px-6">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-4xl font-semibold text-gray-900 md:text-5xl">Frequently Asked Questions</h2>
          </div>
          <div className="mt-16 grid gap-8 md:grid-cols-3">
            {faqs.map((faq) => (
              <div key={faq.question} className="rounded-3xl bg-white p-8 text-left shadow-sm">
                <h3 className="text-lg font-semibold text-gray-900">{faq.question}</h3>
                <p className="mt-3 text-sm text-gray-600">{faq.answer}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
