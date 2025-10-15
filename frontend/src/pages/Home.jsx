import { useNavigate } from "react-router-dom";

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-b from-blue-50 to-white text-gray-800">
      <h1 className="text-4xl font-bold mb-4 text-blue-700">
        Supply Chain Alert System
      </h1>
      <p className="text-lg max-w-2xl text-center mb-8">
        Empower your logistics operations with intelligent disruption detection,
        semantic search, and real-time analytics. Upload your shipment data and get
        instant insights into delays, risks, and disruptions.
      </p>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 max-w-4xl mb-10">
        <FeatureCard title="📊 Analytics Dashboard" desc="Visualize disruptions, delays, and risk scores across your supply chain." />
        <FeatureCard title="🔍 Smart Search" desc="Use semantic search to quickly find similar shipment disruptions." />
        <FeatureCard title="⚙️ AI Insights" desc="Generate summaries and actionable alerts with our AI-powered engine." />
      </div>

      <button
        onClick={() => navigate("/login")}
        className="px-6 py-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition"
      >
        Get Started
      </button>
    </div>
  );
}

function FeatureCard({ title, desc }) {
  return (
    <div className="bg-white shadow-md rounded-xl p-5 border hover:shadow-lg transition">
      <h2 className="font-semibold text-xl mb-2">{title}</h2>
      <p className="text-gray-600">{desc}</p>
    </div>
  );
}
