'use client';

import { useStore } from '@/lib/store';
import { tradingEngine } from '@/lib/trading-engine';
import { AlertTriangle, TrendingUp, CheckCircle, XCircle } from 'lucide-react';

export default function TradingSignals() {
  const { tradingSignals, pendingApprovals } = useStore();

  const handleApprove = async (executionId: string) => {
    await tradingEngine.approveTrade(executionId);
    // Refresh approvals
    const updated = tradingEngine.getPendingApprovals();
    useStore.getState().setPendingApprovals(updated);
  };

  const handleReject = (executionId: string) => {
    tradingEngine.rejectTrade(executionId);
    // Refresh approvals
    const updated = tradingEngine.getPendingApprovals();
    useStore.getState().setPendingApprovals(updated);
  };

  return (
    <div className="bg-slate-800/50 backdrop-blur-lg border border-slate-700 rounded-xl p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-bold">Trading Signals</h2>
        <span className="text-sm text-slate-400">
          {tradingSignals.length} active
        </span>
      </div>

      {pendingApprovals.length > 0 && (
        <div className="mb-6">
          <h3 className="text-sm font-semibold text-yellow-400 mb-3 flex items-center gap-2">
            <AlertTriangle className="w-4 h-4" />
            Pending Approvals ({pendingApprovals.length})
          </h3>
          <div className="space-y-2">
            {pendingApprovals.map((approval) => {
              const executionId = `${approval.market_id}-${approval.timestamp}`;
              return (
                <div
                  key={executionId}
                  className="bg-yellow-500/10 border border-yellow-500/30 rounded-lg p-3"
                >
                  <div className="flex items-start justify-between mb-2">
                    <div>
                      <p className="font-semibold text-sm">{approval.ticker}</p>
                      <p className="text-xs text-slate-400 mt-1">
                        {approval.side.toUpperCase()} x{approval.quantity} @ ${approval.price.toFixed(2)}
                      </p>
                    </div>
                    <span className="text-xs px-2 py-1 bg-yellow-500/20 text-yellow-400 rounded">
                      Edge: {approval.analysis.edge_score.toFixed(1)}%
                    </span>
                  </div>
                  
                  <div className="flex gap-2 mt-3">
                    <button
                      onClick={() => handleApprove(executionId)}
                      className="flex-1 flex items-center justify-center gap-1 px-3 py-1.5 bg-green-600 hover:bg-green-700 rounded text-xs font-medium transition-colors"
                    >
                      <CheckCircle className="w-3 h-3" />
                      Approve
                    </button>
                    <button
                      onClick={() => handleReject(executionId)}
                      className="flex-1 flex items-center justify-center gap-1 px-3 py-1.5 bg-red-600 hover:bg-red-700 rounded text-xs font-medium transition-colors"
                    >
                      <XCircle className="w-3 h-3" />
                      Reject
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      <div className="space-y-3">
        {tradingSignals.length === 0 ? (
          <div className="text-center py-8 text-slate-400 text-sm">
            No active trading signals. Click "Scan Markets" to find opportunities.
          </div>
        ) : (
          tradingSignals.slice(0, 10).map((signal, idx) => (
            <div
              key={`${signal.market.id}-${idx}`}
              className="bg-slate-700/30 border border-slate-600 rounded-lg p-3 hover:bg-slate-700/50 transition-colors"
            >
              <div className="flex items-start justify-between mb-2">
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <p className="font-semibold text-sm">{signal.market.ticker}</p>
                    <span className={`text-xs px-2 py-0.5 rounded ${
                      signal.action === 'buy'
                        ? 'bg-green-500/20 text-green-400'
                        : 'bg-red-500/20 text-red-400'
                    }`}>
                      {signal.action.toUpperCase()}
                    </span>
                  </div>
                  <p className="text-xs text-slate-400 mt-1 line-clamp-1">
                    {signal.market.title}
                  </p>
                </div>
                
                <div className="flex items-center gap-1 ml-2">
                  <TrendingUp className="w-4 h-4 text-green-400" />
                  <span className="text-sm font-bold text-green-400">
                    +{signal.analysis.edge_score.toFixed(1)}%
                  </span>
                </div>
              </div>

              <div className="grid grid-cols-4 gap-2 text-xs mb-2">
                <div>
                  <p className="text-slate-500">Side</p>
                  <p className={`font-semibold ${
                    signal.side === 'yes' ? 'text-green-400' : 'text-red-400'
                  }`}>
                    {signal.side?.toUpperCase()}
                  </p>
                </div>
                <div>
                  <p className="text-slate-500">Size</p>
                  <p className="font-semibold">{signal.size.toFixed(1)}%</p>
                </div>
                <div>
                  <p className="text-slate-500">Confidence</p>
                  <p className="font-semibold">{signal.confidence.toFixed(0)}%</p>
                </div>
                <div>
                  <p className="text-slate-500">Urgency</p>
                  <p className={`font-semibold ${
                    signal.urgency > 70 ? 'text-red-400' :
                    signal.urgency > 40 ? 'text-yellow-400' : 'text-green-400'
                  }`}>
                    {signal.urgency.toFixed(0)}
                  </p>
                </div>
              </div>

              {signal.analysis.insights.length > 0 && (
                <div className="pt-2 border-t border-slate-600">
                  <p className="text-xs text-slate-400">
                    {signal.analysis.insights[0]}
                  </p>
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
}
