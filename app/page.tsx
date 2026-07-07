'use client';

import { useEffect, useState } from 'react';
import { kalshiPublicAPI, PublicMarket } from '@/lib/kalshi-public-api';
import { publicMarketAnalyzer, BettingRecommendation } from '@/lib/public-market-analyzer';
import { TrendingUp, RefreshCw, AlertCircle, CheckCircle, Clock, DollarSign, BarChart3 } from 'lucide-react';

export default function Home() {
  const [recommendations, setRecommendations] = useState<BettingRecommendation[]>([]);
  const [groupedByCategory, setGroupedByCategory] = useState<Map<string, BettingRecommendation[]>>(new Map());
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [lastUpdate, setLastUpdate] = useState<Date | null>(null);
  const [selectedCategory, setSelectedCategory] = useState<string>('All');

  const loadMarkets = async () => {
    setIsLoading(true);
    setError('');
    
    try {
      // Fetch all open markets from Kalshi
      const markets = await kalshiPublicAPI.getMarkets({ limit: 500, status: 'open' });
      
      if (markets.length === 0) {
        setError('No markets found');
        return;
      }

      // Analyze and get best opportunities
      const bestBets = publicMarketAnalyzer.analyzeBestOpportunities(markets);
      setRecommendations(bestBets);
      
      // Group by category
      const grouped = publicMarketAnalyzer.groupByCategory(bestBets);
      setGroupedByCategory(grouped);
      
      setLastUpdate(new Date());
    } catch (err) {
      console.error('Failed to load markets:', err);
      setError('Failed to load market data. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadMarkets();
    
    // Auto-refresh every 5 minutes
    const interval = setInterval(loadMarkets, 5 * 60 * 1000);
    return () => clearInterval(interval);
  }, []);

  const categories = ['All', ...Array.from(groupedByCategory.keys())].sort();
  const displayedRecs = selectedCategory === 'All' 
    ? recommendations 
    : groupedByCategory.get(selectedCategory) || [];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white">
      {/* Header */}
      <header className="border-b border-slate-700 bg-slate-900/50 backdrop-blur-lg sticky top-0 z-50">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
                Kalshi Best Bets Analyzer
              </h1>
              <p className="text-sm text-slate-400 mt-1">
                AI-powered analysis of prediction markets • No login required
              </p>
            </div>
            
            <button
              onClick={loadMarkets}
              disabled={isLoading}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-700 rounded-lg transition-colors"
            >
              <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
              {isLoading ? 'Analyzing...' : 'Refresh'}
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-6 py-8">
        {/* Stats */}
        {!isLoading && recommendations.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <StatCard
              icon={<TrendingUp className="w-6 h-6" />}
              label="Best Opportunities"
              value={recommendations.length.toString()}
              subtitle="Markets analyzed"
            />
            <StatCard
              icon={<BarChart3 className="w-6 h-6" />}
              label="Categories"
              value={groupedByCategory.size.toString()}
              subtitle="Different markets"
            />
            <StatCard
              icon={<CheckCircle className="w-6 h-6" />}
              label="Strong Buys"
              value={recommendations.filter(r => r.recommendation === 'STRONG BUY').length.toString()}
              subtitle="High confidence"
            />
            <StatCard
              icon={<Clock className="w-6 h-6" />}
              label="Last Updated"
              value={lastUpdate ? lastUpdate.toLocaleTimeString() : '--'}
              subtitle="Auto-refreshes"
            />
          </div>
        )}

        {/* Category Filter */}
        {!isLoading && recommendations.length > 0 && (
          <div className="mb-6 flex gap-2 flex-wrap">
            {categories.map(cat => (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  selectedCategory === cat
                    ? 'bg-blue-600 text-white'
                    : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
                }`}
              >
                {cat} {cat !== 'All' && `(${groupedByCategory.get(cat)?.length || 0})`}
              </button>
            ))}
          </div>
        )}

        {/* Loading State */}
        {isLoading && (
          <div className="text-center py-20">
            <RefreshCw className="w-12 h-12 animate-spin mx-auto mb-4 text-blue-400" />
            <p className="text-xl text-slate-300">Analyzing Kalshi markets...</p>
            <p className="text-sm text-slate-500 mt-2">Finding the best betting opportunities for you</p>
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-6 text-center">
            <AlertCircle className="w-12 h-12 mx-auto mb-4 text-red-400" />
            <p className="text-red-400">{error}</p>
            <button
              onClick={loadMarkets}
              className="mt-4 px-4 py-2 bg-red-600 hover:bg-red-700 rounded-lg"
            >
              Try Again
            </button>
          </div>
        )}

        {/* Recommendations */}
        {!isLoading && !error && displayedRecs.length > 0 && (
          <div className="space-y-4">
            {displayedRecs.map((rec) => (
              <RecommendationCard key={rec.ticker} recommendation={rec} />
            ))}
          </div>
        )}

        {/* No Results */}
        {!isLoading && !error && displayedRecs.length === 0 && recommendations.length > 0 && (
          <div className="text-center py-20 text-slate-400">
            No opportunities found in this category
          </div>
        )}
      </main>
    </div>
  );
}

function StatCard({ icon, label, value, subtitle }: any) {
  return (
    <div className="bg-slate-800/50 backdrop-blur-lg border border-slate-700 rounded-xl p-6">
      <div className="flex items-center justify-between mb-4">
        <div className="p-2 bg-blue-500/10 rounded-lg text-blue-400">
          {icon}
        </div>
      </div>
      <p className="text-sm text-slate-400 mb-1">{label}</p>
      <p className="text-2xl font-bold">{value}</p>
      {subtitle && <p className="text-xs text-slate-500 mt-1">{subtitle}</p>}
    </div>
  );
}

function RecommendationCard({ recommendation }: { recommendation: BettingRecommendation }) {
  const rec = recommendation;
  
  return (
    <div className="bg-slate-800/50 backdrop-blur-lg border border-slate-700 rounded-xl p-6 hover:bg-slate-800/70 transition-colors">
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-2">
            <span className={`px-3 py-1 rounded-full text-xs font-bold ${
              rec.recommendation === 'STRONG BUY' ? 'bg-green-500/20 text-green-400' :
              rec.recommendation === 'BUY' ? 'bg-blue-500/20 text-blue-400' : 'bg-slate-500/20 text-slate-400'
            }`}>
              {rec.recommendation}
            </span>
            <span className="text-xs px-2 py-1 bg-slate-700 rounded">{rec.category}</span>
          </div>
          <h3 className="text-lg font-semibold mb-1">{rec.title}</h3>
          <p className="text-xs text-slate-500">Ticker: {rec.ticker}</p>
        </div>
        
        <div className="text-right">
          <div className="text-3xl font-bold text-green-400">
            {rec.edge_percentage > 0 ? '+' : ''}{rec.edge_percentage.toFixed(1)}%
          </div>
          <p className="text-xs text-slate-400">Edge</p>
        </div>
      </div>

      {/* Recommendation */}
      <div className="grid grid-cols-2 gap-4 mb-4 p-4 bg-slate-700/30 rounded-lg">
        <div>
          <p className="text-xs text-slate-400 mb-1">Recommended Side</p>
          <p className={`text-2xl font-bold ${rec.recommended_side === 'YES' ? 'text-green-400' : 'text-red-400'}`}>
            {rec.recommended_side}
          </p>
        </div>
        <div>
          <p className="text-xs text-slate-400 mb-1">Current Price</p>
          <p className="text-2xl font-bold">${rec.current_price.toFixed(2)}</p>
        </div>
      </div>

      {/* Metrics */}
      <div className="grid grid-cols-4 gap-3 mb-4">
        <Metric label="Confidence" value={`${rec.confidence_score}%`} />
        <Metric label="Risk" value={rec.risk_level} 
          color={rec.risk_level === 'LOW' ? 'text-green-400' : rec.risk_level === 'MEDIUM' ? 'text-yellow-400' : 'text-red-400'} />
        <Metric label="Liquidity" value={`$${(rec.liquidity / 1000).toFixed(1)}K`} />
        <Metric label="Urgency" value={rec.urgency} 
          color={rec.urgency === 'HIGH' ? 'text-red-400' : rec.urgency === 'MEDIUM' ? 'text-yellow-400' : 'text-green-400'} />
      </div>

      {/* Reasons */}
      {rec.reasons.length > 0 && (
        <div className="mb-4">
          <p className="text-xs font-semibold text-slate-300 mb-2">Why this bet:</p>
          <div className="space-y-1">
            {rec.reasons.map((reason, idx) => (
              <div key={idx} className="flex items-start gap-2 text-xs text-slate-400">
                <CheckCircle className="w-3 h-3 text-green-400 mt-0.5 flex-shrink-0" />
                <span>{reason}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Warnings */}
      {rec.warnings.length > 0 && (
        <div className="p-3 bg-yellow-500/10 border border-yellow-500/30 rounded-lg">
          <div className="space-y-1">
            {rec.warnings.map((warning, idx) => (
              <div key={idx} className="flex items-start gap-2 text-xs text-yellow-400">
                <AlertCircle className="w-3 h-3 mt-0.5 flex-shrink-0" />
                <span>{warning}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Additional Info */}
      <div className="mt-4 pt-4 border-t border-slate-600 text-xs text-slate-500">
        <div className="flex justify-between">
          <span>Closes in {rec.closes_in_hours.toFixed(0)} hours</span>
          <span>24h Volume: ${(rec.volume_24h / 1000).toFixed(1)}K</span>
        </div>
      </div>
    </div>
  );
}

function Metric({ label, value, color = 'text-white' }: any) {
  return (
    <div>
      <p className="text-xs text-slate-500 mb-1">{label}</p>
      <p className={`font-semibold ${color}`}>{value}</p>
    </div>
  );
}
