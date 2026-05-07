"use client";

import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

const processingTrend = [
  { month: "Jan", days: 124 },
  { month: "Feb", days: 118 },
  { month: "Mar", days: 132 },
  { month: "Apr", days: 127 },
  { month: "May", days: 116 },
  { month: "Jun", days: 109 },
];

export function ProcessingPreviewChartInner() {
  return (
    <div className="h-64 min-h-64 w-full min-w-0">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={processingTrend} margin={{ left: 4, right: 8, top: 8 }}>
          <defs>
            <linearGradient id="processing" x1="0" x2="0" y1="0" y2="1">
              <stop offset="5%" stopColor="#0f766e" stopOpacity={0.28} />
              <stop offset="95%" stopColor="#0f766e" stopOpacity={0.02} />
            </linearGradient>
          </defs>
          <CartesianGrid stroke="#e5e7eb" strokeDasharray="3 3" vertical={false} />
          <XAxis dataKey="month" tickLine={false} axisLine={false} />
          <YAxis tickLine={false} axisLine={false} width={36} />
          <Tooltip
            contentStyle={{
              border: "1px solid #d1d5db",
              borderRadius: 8,
              boxShadow: "0 12px 24px rgba(15, 23, 42, 0.08)",
            }}
            formatter={(value) => [`${value} days`, "Average wait"]}
          />
          <Area
            type="monotone"
            dataKey="days"
            stroke="#0f766e"
            strokeWidth={2}
            fill="url(#processing)"
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
