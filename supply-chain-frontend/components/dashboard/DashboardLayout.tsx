'use client';

import RiskHeatmap from './RiskHeatmap';
import TrendsChart from './TrendsChart';
import AlertsTable from './AlertsTable';
import RootCauseCard from './RootCauseCard';

export default function DashboardLayout() {
  return (
    <div className="min-h-screen bg-[#0B0F19] text-gray-100 p-8">
      <header className="flex justify-between items-center mb-10">
        <h1 className="text-3xl font-semibold">Supply Chain Risk Dashboard</h1>
        <nav className="space-x-6 text-gray-400">
          <button className="hover:text-white">Dashboard</button>
          <button className="hover:text-white">Alerts</button>
          <button className="hover:text-white">Trends</button>
        </nav>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 bg-[#111827] p-6 rounded-xl shadow-md">
          <h2 className="text-lg mb-4 font-semibold">Risk Heatmap</h2>
          <RiskHeatmap />
        </div>

        <div className="bg-[#111827] p-6 rounded-xl shadow-md">
          <h2 className="text-lg mb-4 font-semibold">Trends over Time</h2>
          <TrendsChart />
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mt-8">
        <div className="lg:col-span-2 bg-[#111827] p-6 rounded-xl shadow-md">
          <h2 className="text-lg mb-4 font-semibold">Alerts</h2>
          <AlertsTable />
        </div>

        <div className="bg-[#111827] p-6 rounded-xl shadow-md">
          <h2 className="text-lg mb-4 font-semibold">Root Cause Analysis</h2>
          <RootCauseCard />
        </div>
      </div>
    </div>
  );
}
