export default function Footer() {
  const year = new Date().getFullYear();

  return (
    <footer className="border-t border-gray-200 bg-white py-10">
      <div className="mx-auto flex max-w-6xl flex-col items-center gap-4 px-6 text-sm text-gray-500 md:flex-row md:justify-between">
        <p>© {year} Zeusss. AI Supply Chain Dashboard and Analytics.</p>
        <div className="flex gap-6">
          <a href="#features" className="transition hover:text-gray-900">
            Features
          </a>
          <a href="#steps" className="transition hover:text-gray-900">
            Getting started
          </a>
          <a href="#faq" className="transition hover:text-gray-900">
            FAQ
          </a>
        </div>
      </div>
    </footer>
  );
}
