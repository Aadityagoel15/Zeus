'use client';

import { useEffect, useState } from 'react';
import { fetchData } from '../../lib/apiClient';

export default function RiskHeatmap() {
  const [locations, setLocations] = useState<any[]>([]);

  useEffect(() => {
    fetchData('/insights/heatmap')
      .then((data: any[]) => setLocations(data))
      .catch(console.error);
  }, []);

  return (
    <div className="bg-[#0A0A0A] p-4 rounded-xl shadow-md">
      <h2 className="text-xl font-semibold mb-4">Risk Heatmap</h2>
      {/* Replace with react-simple-maps visualization later */}
      <pre className="text-gray-400">{JSON.stringify(locations, null, 2)}</pre>
    </div>
  );
}
