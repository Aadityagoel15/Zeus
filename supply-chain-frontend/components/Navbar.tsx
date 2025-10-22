export default function Navbar() {
  return (
    <nav className="fixed top-0 z-50 w-full border-b border-gray-200 bg-white">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
        <div className="flex items-center gap-2">
          <span className="text-2xl font-semibold text-gray-900">Woyage</span>
          <span className="rounded-full bg-indigo-100 px-3 py-1 text-xs font-medium text-indigo-600">
            Analytics
          </span>
        </div>
        <div className="hidden items-center gap-8 text-sm font-medium text-gray-600 md:flex">
          <a href="#features" className="transition hover:text-gray-900">
            Features
          </a>
          <a href="#steps" className="transition hover:text-gray-900">
            How it works
          </a>
          <a href="#stack" className="transition hover:text-gray-900">
            Stack
          </a>
          <a href="#faq" className="transition hover:text-gray-900">
            FAQ
          </a>
        </div>
        <a
          href="#get-started"
          className="rounded-full bg-gray-900 px-5 py-2 text-sm font-semibold text-white transition hover:bg-gray-700"
        >
          Get Started
        </a>
      </div>
    </nav>
  );
}
