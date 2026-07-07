'use client';

import { useEffect, useState } from 'react';
import { useStore } from '@/lib/store';
import { kalshiAPI } from '@/lib/kalshi-api';
import { marketAnalyzer } from '@/lib/market-analyzer';
import { tradingEngine } from '@/lib/trading-engine';
import { riskManager } from '@/lib/risk-manager';
import MarketList from './MarketList';
import PortfolioOverview from './PortfolioOverview';
import TradingSignals from './TradingSignals';
import RiskMonitor from './RiskMonitor';
import PerformanceChart from './PerformanceChart';
import { RefreshCw, TrendingUp, Activity, DollarSign } from 'lucide-react';

export default function Dashboard() {
  const {
    balance,
    positions,
    markets,
    analyses,
    tradingSignals,
    portfolioRisk,
    isAutoTrading,
    setMarkets,
    setAnalyses,
    setBalance,
    setPositions,
    setTradingSignals,
    setPortfolioRisk,
    setAutoTrading,
  } = useStore();

  const [isScanning, setIsScanning] = useState(false);
  const [autoRefresh, setAutoRefresh] = useState(true);

  useEffect(() => {
    // Initial data load
    loadDashboardData();

    // Set up auto-refresh
    if (autoRefresh) {
      const interval = setInterval(loadDashboardData, 30000); // Every 30 seconds
      return () => clearInterval(interval);
    }
  }, [autoRefresh]);

  const loadDashboardData = async () => {
    try {
      // Load balance
      const balanceData = await kalshiAPI.getBalance();
      if (balanceData) setBalance(balanceData);

      // Load positions
      const positionsData = await kalshiAPI.getPositions();
      setPositions(positionsData);

      // Calculate portfolio risk
      if (balanceData) {
        const risk = riskManager.calculatePortfolioRisk(balanceData, positionsData);
        setPortfolioRisk(risk);
      }

      // Load markets (limit to 50 for performance)
      const marketsData = await kalshiAPI.getMarkets({ status: 'open', limit: 50 });
      setMarkets(marketsData);
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
    }
  };

  const handleScanMarkets = async () => {
    setIsScanning(true);
    try {
      // Get markets
      const marketsData = await kalshiAPI.getMarkets({ status: 'open', limit: 100 });
      setMarkets(marketsData);

      // Analyze markets
      const analysesData = await marketAnalyzer.analyzeMultipleMarkets(marketsData);
      setAnalyses(analysesData);

      // Get trading signals
      const signals = await tradingEngine.scanMarkets();
      setTradingSignals(signals);
    } catch (error) {
      console.error('Market scan failed:', error);
    } finally {
      setIsScanning(false);
    }
  };

  const handleToggleAutoTrading = async () => {
    if (!isAutoTrading) {
      tradingEngine.updateConfig({ autoTradeEnabled: true });
      await tradingEngine.start();
      setAutoTrading(true);
    } else {
      tradingEngine.stop();
      tradingEngine.updateConfig({ autoTradeEnabled: false });
      setAutoTrading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white">
      {/* Header */}
      <header className="border-b border-slate-700 bg-slate-900/50 backdrop-blur-lg">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
                Kalshi Trading Platform
              </h1>
              <p className="text-sm text-slate-400 mt-1">Advanced Market Analysis & Automated Trading</p>
            </div>
            
            <div className="flex items-center gap-4">
              <button
                onClick={() => setAutoRefresh(!autoRefresh)}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  autoRefresh
                    ? 'bg-green-600 hover:bg-green-700'
                    : 'bg-slate-700 hover:bg-slate-600'
                }`}
              >
                Auto Refresh: {autoRefresh ? 'ON' : 'OFF'}
              </button>
              
              <button
                onClick={handleScanMarkets}
                disabled={isScanning}
                className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-sm font-medium transition-colors disabled:opacity-50"
              >
                <RefreshCw className={`w-4 h-4 ${isScanning ? 'animate-spin' : ''}`} />
                {isScanning ? 'Scanning...' : 'Scan Markets'}
              </button>
              
              <button
                onClick={handleToggleAutoTrading}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  isAutoTrading
                    ? 'bg-red-600 hover:bg-red-700'
                    : 'bg-green-600 hover:bg-green-700'
                }`}
              >
                {isAutoTrading ? 'Stop Auto-Trading' : 'Start Auto-Trading'}
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-6 py-8">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <StatCard
            icon={<DollarSign className="w-6 h-6" />}
            label="Portfolio Value"
            value={`$${balance?.balance.toFixed(2) || '0.00'}`}
            change="+5.2%"
            positive={true}
          />
          <StatCard
            icon={<TrendingUp className="w-6 h-6" />}
            label="Open Positions"
            value={positions.length.toString()}
            subtitle={`Max: ${riskManager.getLimits().maxConcurrentPositions}`}
          />
          <StatCard
            icon={<Activity className="w-6 h-6" />}
            label="Trading Signals"
            value={tradingSignals.length.toString()}
            subtitle="Active opportunities"
          />
          <StatCard
            icon={<Activity className="w-6 h-6" />}
            label="Risk Score"
            value={portfolioRisk?.riskScore.toFixed(0) || '0'}
            subtitle={`/100 - ${portfolioRisk?.canTrade ? 'Can Trade' : 'Trading Halted'}`}
            positive={portfolioRisk ? portfolioRisk.riskScore < 50 : true}
          />
        </div>

        {/* Main Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          <div className="lg:col-span-2">
            <PerformanceChart />
          </div>
          <div>
            <RiskMonitor />
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <PortfolioOverview />
          <TradingSignals />
        </div>

        <div>
          <MarketList />
        </div>
      </main>
    </div>
  );
}

function StatCard({
  icon,
  label,
  value,
  change,
  subtitle,
  positive = true,
}: {
  icon: React.ReactNode;
  label: string;
  value: string;
  change?: string;
  subtitle?: string;
  positive?: boolean;
}) {
  return (
    <div className="bg-slate-800/50 backdrop-blur-lg border border-slate-700 rounded-xl p-6">
      <div className="flex items-center justify-between mb-4">
        <div className="p-2 bg-blue-500/10 rounded-lg text-blue-400">
          {icon}
        </div>
        {change && (
          <span className={`text-sm font-medium ${positive ? 'text-green-400' : 'text-red-400'}`}>
            {change}
          </span>
        )}
      </div>
      <div>
        <p className="text-sm text-slate-400 mb-1">{label}</p>
        <p className="text-2xl font-bold">{value}</p>
        {subtitle && <p className="text-xs text-slate-500 mt-1">{subtitle}</p>}
      </div>
    </div>
  );
}
