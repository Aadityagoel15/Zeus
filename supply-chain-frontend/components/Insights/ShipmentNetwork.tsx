// components/Insights/ShipmentNetwork.tsx
"use client";

import dynamic from "next/dynamic";
import { useEffect, useState } from "react";

const ForceGraph2D = dynamic(() => import("react-force-graph").then(mod => mod.ForceGraph2D), { ssr: false });

interface Shipment {
  origin: string;
  destination: string;
  risk_score: number;
}

export default function ShipmentNetwork() {
  const [data, setData] = useState({ nodes: [], links: [] });

  useEffect(() => {
    fetch("/api/insights/metrics")
      .then(res => res.json())
      .then(metrics => {
        const shipments: Shipment[] = metrics.shipments || [];
        const nodes = Array.from(
          new Set(shipments.flatMap(s => [s.origin, s.destination]))
        ).map(id => ({ id }));

        const links = shipments.map(s => ({
          source: s.origin,
          target: s.destination,
          value: s.risk_score,
        }));

        setData({ nodes, links });
      })
      .catch(console.error);
  }, []);

  return (
    <div className="w-full h-[600px] border rounded-lg p-2">
      <ForceGraph2D
        graphData={data}
        nodeAutoColorBy="id"
        linkDirectionalParticles={2}
        linkDirectionalParticleSpeed={d => (d.value as number) * 0.01}
      />
    </div>
  );
}
