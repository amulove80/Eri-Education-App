'use client';

import { useStore } from '@/lib/store';
import { TrendingUp, TrendingDown, DollarSign } from 'lucide-react';

export default function PortfolioOverview() {
  const { positions, balance } = useStore();

  const totalPnL = positions.reduce((sum, p) => sum + p.pnl, 0);
  const totalValue = positions.reduce((sum, p) => sum + p.current_value, 0);

  return (
    <div className="bg-slate-800/50 backdrop-blur-lg border border-slate-700 rounded-xl p-6">
      <h2 className="text-xl font-bold mb-6">Portfolio Overview</h2>

      <div className="grid grid-cols-2 gap-4 mb-6">
        <div className="bg-slate-700/30 rounded-lg p-4">
          <p className="text-sm text-slate-400 mb-1">Total Value</p>
          <p className="text-2xl font-bold">${balance?.balance.toFixed(2) || '0.00'}</p>
        </div>
        <div className="bg-slate-700/30 rounded-lg p-4">
          <p className="text-sm text-slate-400 mb-1">Available</p>
          <p className="text-2xl font-bold">${balance?.available_balance.toFixed(2) || '0.00'}</p>
        </div>
        <div className={`rounded-lg p-4 ${
          totalPnL >= 0 ? 'bg-green-500/10' : 'bg-red-500/10'
        }`}>
          <p className="text-sm text-slate-400 mb-1">Total P&L</p>
          <div className="flex items-center gap-2">
            {totalPnL >= 0 ? (
              <TrendingUp className="w-5 h-5 text-green-400" />
            ) : (
              <TrendingDown className="w-5 h-5 text-red-400" />
            )}
            <p className={`text-2xl font-bold ${
              totalPnL >= 0 ? 'text-green-400' : 'text-red-400'
            }`}>
              ${Math.abs(totalPnL).toFixed(2)}
            </p>
          </div>
        </div>
        <div className="bg-slate-700/30 rounded-lg p-4">
          <p className="text-sm text-slate-400 mb-1">Position Value</p>
          <p className="text-2xl font-bold">${totalValue.toFixed(2)}</p>
        </div>
      </div>

      <div className="space-y-3">
        <div className="flex items-center justify-between mb-2">
          <h3 className="font-semibold text-sm">Open Positions ({positions.length})</h3>
        </div>
        
        {positions.length === 0 ? (
          <div className="text-center py-8 text-slate-400 text-sm">
            No open positions
          </div>
        ) : (
          positions.map(position => (
            <div
              key={position.market_id}
              className="bg-slate-700/30 border border-slate-600 rounded-lg p-3"
            >
              <div className="flex items-start justify-between mb-2">
                <div className="flex-1">
                  <p className="font-semibold text-sm">{position.market_id}</p>
                  <div className="flex items-center gap-2 mt-1">
                    <span className={`text-xs px-2 py-0.5 rounded ${
                      position.side === 'yes'
                        ? 'bg-green-500/20 text-green-400'
                        : 'bg-red-500/20 text-red-400'
                    }`}>
                      {position.side.toUpperCase()}
                    </span>
                    <span className="text-xs text-slate-400">
                      {position.position} contracts @ ${position.average_price.toFixed(2)}
                    </span>
                  </div>
                </div>
                
                <div className={`text-right ${
                  position.pnl >= 0 ? 'text-green-400' : 'text-red-400'
                }`}>
                  <p className="text-sm font-bold">
                    {position.pnl >= 0 ? '+' : ''}${position.pnl.toFixed(2)}
                  </p>
                  <p className="text-xs">
                    {((position.pnl / position.total_cost) * 100).toFixed(1)}%
                  </p>
                </div>
              </div>
              
              <div className="grid grid-cols-3 gap-2 text-xs">
                <div>
                  <p className="text-slate-500">Cost</p>
                  <p className="font-semibold">${position.total_cost.toFixed(2)}</p>
                </div>
                <div>
                  <p className="text-slate-500">Value</p>
                  <p className="font-semibold">${position.current_value.toFixed(2)}</p>
                </div>
                <div>
                  <p className="text-slate-500">Return</p>
                  <p className={`font-semibold ${
                    position.pnl >= 0 ? 'text-green-400' : 'text-red-400'
                  }`}>
                    {((position.pnl / position.total_cost) * 100).toFixed(1)}%
                  </p>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
