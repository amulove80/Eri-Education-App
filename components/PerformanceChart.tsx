'use client';

import { useStore } from '@/lib/store';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';

export default function PerformanceChart() {
  const { balance, positions } = useStore();

  // Generate mock historical data for demonstration
  // In production, this would come from actual trade history
  const generateMockData = () => {
    const data = [];
    const baseValue = balance?.balance || 10000;
    const now = Date.now();
    
    for (let i = 30; i >= 0; i--) {
      const date = new Date(now - i * 24 * 60 * 60 * 1000);
      const randomChange = (Math.random() - 0.48) * 200; // Slight upward bias
      const portfolioValue = baseValue + (30 - i) * randomChange;
      
      data.push({
        date: date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
        portfolio: Math.max(baseValue * 0.8, portfolioValue),
        benchmark: baseValue,
      });
    }
    
    return data;
  };

  const data = generateMockData();

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-slate-800 border border-slate-600 rounded-lg p-3">
          <p className="text-sm text-slate-400 mb-2">{payload[0].payload.date}</p>
          <p className="text-sm font-semibold text-blue-400">
            Portfolio: ${payload[0].value.toFixed(2)}
          </p>
          <p className="text-sm font-semibold text-slate-400">
            Benchmark: ${payload[1].value.toFixed(2)}
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="bg-slate-800/50 backdrop-blur-lg border border-slate-700 rounded-xl p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-xl font-bold">Performance</h2>
          <p className="text-sm text-slate-400 mt-1">30-day portfolio value</p>
        </div>
        
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-blue-500 rounded-full" />
            <span className="text-xs text-slate-400">Portfolio</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-slate-500 rounded-full" />
            <span className="text-xs text-slate-400">Benchmark</span>
          </div>
        </div>
      </div>

      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data} margin={{ top: 5, right: 5, left: 5, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
          <XAxis
            dataKey="date"
            stroke="#94a3b8"
            style={{ fontSize: '12px' }}
            tickLine={false}
          />
          <YAxis
            stroke="#94a3b8"
            style={{ fontSize: '12px' }}
            tickLine={false}
            tickFormatter={(value) => `$${(value / 1000).toFixed(1)}k`}
          />
          <Tooltip content={<CustomTooltip />} />
          <Line
            type="monotone"
            dataKey="portfolio"
            stroke="#3b82f6"
            strokeWidth={2}
            dot={false}
            activeDot={{ r: 4 }}
          />
          <Line
            type="monotone"
            dataKey="benchmark"
            stroke="#64748b"
            strokeWidth={2}
            strokeDasharray="5 5"
            dot={false}
          />
        </LineChart>
      </ResponsiveContainer>

      <div className="grid grid-cols-4 gap-4 mt-6 pt-6 border-t border-slate-600">
        <Stat label="Win Rate" value="62.5%" positive />
        <Stat label="Total Trades" value="24" />
        <Stat label="Avg Return" value="+4.2%" positive />
        <Stat label="Sharpe Ratio" value="1.8" />
      </div>
    </div>
  );
}

function Stat({
  label,
  value,
  positive = false,
}: {
  label: string;
  value: string;
  positive?: boolean;
}) {
  return (
    <div>
      <p className="text-xs text-slate-400 mb-1">{label}</p>
      <p className={`text-lg font-bold ${
        positive ? 'text-green-400' : 'text-slate-200'
      }`}>
        {value}
      </p>
    </div>
  );
}
