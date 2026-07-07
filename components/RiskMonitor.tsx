'use client';

import { useStore } from '@/lib/store';
import { riskManager } from '@/lib/risk-manager';
import { Shield, AlertTriangle, CheckCircle } from 'lucide-react';

export default function RiskMonitor() {
  const { portfolioRisk, balance, positions } = useStore();
  const limits = riskManager.getLimits();

  if (!portfolioRisk) {
    return (
      <div className="bg-slate-800/50 backdrop-blur-lg border border-slate-700 rounded-xl p-6">
        <h2 className="text-xl font-bold mb-6">Risk Monitor</h2>
        <div className="text-center py-8 text-slate-400 text-sm">
          Loading risk data...
        </div>
      </div>
    );
  }

  const getRiskColor = (score: number) => {
    if (score < 30) return 'text-green-400';
    if (score < 60) return 'text-yellow-400';
    return 'text-red-400';
  };

  const getRiskBgColor = (score: number) => {
    if (score < 30) return 'bg-green-500/20';
    if (score < 60) return 'bg-yellow-500/20';
    return 'bg-red-500/20';
  };

  return (
    <div className="bg-slate-800/50 backdrop-blur-lg border border-slate-700 rounded-xl p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-bold">Risk Monitor</h2>
        <Shield className="w-5 h-5 text-blue-400" />
      </div>

      {/* Risk Score */}
      <div className={`${getRiskBgColor(portfolioRisk.riskScore)} rounded-lg p-4 mb-6`}>
        <div className="flex items-center justify-between mb-2">
          <p className="text-sm text-slate-300">Overall Risk Score</p>
          <span className={`text-2xl font-bold ${getRiskColor(portfolioRisk.riskScore)}`}>
            {portfolioRisk.riskScore.toFixed(0)}/100
          </span>
        </div>
        <div className="w-full bg-slate-700 rounded-full h-2">
          <div
            className={`h-2 rounded-full transition-all ${
              portfolioRisk.riskScore < 30 ? 'bg-green-500' :
              portfolioRisk.riskScore < 60 ? 'bg-yellow-500' : 'bg-red-500'
            }`}
            style={{ width: `${portfolioRisk.riskScore}%` }}
          />
        </div>
      </div>

      {/* Trading Status */}
      <div className={`rounded-lg p-4 mb-6 ${
        portfolioRisk.canTrade
          ? 'bg-green-500/10 border border-green-500/30'
          : 'bg-red-500/10 border border-red-500/30'
      }`}>
        <div className="flex items-center gap-2">
          {portfolioRisk.canTrade ? (
            <>
              <CheckCircle className="w-5 h-5 text-green-400" />
              <div>
                <p className="font-semibold text-green-400">Trading Enabled</p>
                <p className="text-xs text-slate-400">All risk checks passed</p>
              </div>
            </>
          ) : (
            <>
              <AlertTriangle className="w-5 h-5 text-red-400" />
              <div>
                <p className="font-semibold text-red-400">Trading Halted</p>
                <p className="text-xs text-slate-400">{portfolioRisk.reasons[0]}</p>
              </div>
            </>
          )}
        </div>
      </div>

      {/* Risk Metrics */}
      <div className="space-y-4">
        <RiskMetric
          label="Portfolio Exposure"
          value={portfolioRisk.totalExposure}
          limit={limits.maxTotalExposure}
          unit="%"
        />
        
        <RiskMetric
          label="Open Positions"
          value={portfolioRisk.positionCount}
          limit={limits.maxConcurrentPositions}
          unit=""
        />
        
        <RiskMetric
          label="Daily P&L"
          value={portfolioRisk.dailyPnL}
          limit={balance ? (balance.balance * limits.maxDailyLoss) / 100 : 0}
          unit="$"
          showNegative
        />
      </div>

      {/* Risk Limits */}
      <div className="mt-6 pt-6 border-t border-slate-600">
        <h3 className="text-sm font-semibold mb-3">Risk Limits</h3>
        <div className="space-y-2 text-xs">
          <div className="flex justify-between">
            <span className="text-slate-400">Max Position Size</span>
            <span className="font-semibold">{limits.maxPositionSize}%</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-400">Max Loss Per Trade</span>
            <span className="font-semibold">{limits.maxLossPerTrade}%</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-400">Min Confidence</span>
            <span className="font-semibold">{limits.minConfidence}%</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-400">Min Liquidity</span>
            <span className="font-semibold">{limits.minLiquidity}</span>
          </div>
        </div>
      </div>

      {/* Warnings */}
      {portfolioRisk.reasons.length > 0 && (
        <div className="mt-6 pt-6 border-t border-slate-600">
          <h3 className="text-sm font-semibold mb-3 text-yellow-400 flex items-center gap-2">
            <AlertTriangle className="w-4 h-4" />
            Warnings
          </h3>
          <div className="space-y-2">
            {portfolioRisk.reasons.map((reason, idx) => (
              <div key={idx} className="text-xs text-slate-300 bg-yellow-500/10 rounded p-2">
                {reason}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

function RiskMetric({
  label,
  value,
  limit,
  unit,
  showNegative = false,
}: {
  label: string;
  value: number;
  limit: number;
  unit: string;
  showNegative?: boolean;
}) {
  const percentage = limit > 0 ? Math.min(100, (Math.abs(value) / limit) * 100) : 0;
  const isWarning = percentage > 70;
  const isDanger = percentage > 90;

  return (
    <div>
      <div className="flex items-center justify-between mb-2">
        <p className="text-sm text-slate-400">{label}</p>
        <span className="text-sm font-semibold">
          {showNegative && value < 0 ? '-' : ''}
          {unit === '$' ? unit : ''}
          {Math.abs(value).toFixed(unit === '$' ? 2 : 0)}
          {unit !== '$' ? unit : ''} / {unit === '$' ? unit : ''}{limit.toFixed(unit === '$' ? 0 : 0)}{unit !== '$' ? unit : ''}
        </span>
      </div>
      <div className="w-full bg-slate-700 rounded-full h-2">
        <div
          className={`h-2 rounded-full transition-all ${
            isDanger ? 'bg-red-500' : isWarning ? 'bg-yellow-500' : 'bg-green-500'
          }`}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}
