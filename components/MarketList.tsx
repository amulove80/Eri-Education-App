'use client';

import { useState } from 'react';
import { useStore } from '@/lib/store';
import { Market } from '@/lib/kalshi-api';
import { TrendingUp, TrendingDown, Clock, DollarSign } from 'lucide-react';

export default function MarketList() {
  const { markets, analyses } = useStore();
  const [filter, setFilter] = useState<'all' | 'high-edge' | 'high-volume'>('all');
  const [sortBy, setSortBy] = useState<'edge' | 'volume' | 'liquidity'>('edge');

  const getAnalysisForMarket = (marketId: string) => {
    return analyses.find(a => a.market_id === marketId);
  };

  const filteredMarkets = markets.filter(market => {
    const analysis = getAnalysisForMarket(market.id);
    if (!analysis) return filter === 'all';
    
    if (filter === 'high-edge') {
      return Math.abs(analysis.edge_score) > 8;
    } else if (filter === 'high-volume') {
      return market.volume > 10000;
    }
    return true;
  });

  const sortedMarkets = [...filteredMarkets].sort((a, b) => {
    if (sortBy === 'edge') {
      const analysisA = getAnalysisForMarket(a.id);
      const analysisB = getAnalysisForMarket(b.id);
      const edgeA = analysisA ? Math.abs(analysisA.edge_score) : 0;
      const edgeB = analysisB ? Math.abs(analysisB.edge_score) : 0;
      return edgeB - edgeA;
    } else if (sortBy === 'volume') {
      return b.volume - a.volume;
    } else {
      return b.liquidity - a.liquidity;
    }
  });

  return (
    <div className="bg-slate-800/50 backdrop-blur-lg border border-slate-700 rounded-xl p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-bold">Market Analysis</h2>
        
        <div className="flex gap-2">
          <select
            value={filter}
            onChange={(e) => setFilter(e.target.value as any)}
            className="px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-sm"
          >
            <option value="all">All Markets</option>
            <option value="high-edge">High Edge</option>
            <option value="high-volume">High Volume</option>
          </select>
          
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as any)}
            className="px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-sm"
          >
            <option value="edge">Sort by Edge</option>
            <option value="volume">Sort by Volume</option>
            <option value="liquidity">Sort by Liquidity</option>
          </select>
        </div>
      </div>

      <div className="space-y-3">
        {sortedMarkets.slice(0, 20).map(market => {
          const analysis = getAnalysisForMarket(market.id);
          return <MarketCard key={market.id} market={market} analysis={analysis} />;
        })}
        
        {sortedMarkets.length === 0 && (
          <div className="text-center py-12 text-slate-400">
            No markets found. Click "Scan Markets" to load data.
          </div>
        )}
      </div>
    </div>
  );
}

function MarketCard({ market, analysis }: { market: Market; analysis?: any }) {
  const edge = analysis?.edge_score || 0;
  const isPositiveEdge = edge > 0;
  
  return (
    <div className="bg-slate-700/30 border border-slate-600 rounded-lg p-4 hover:bg-slate-700/50 transition-colors">
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-1">
            <h3 className="font-semibold text-sm">{market.ticker}</h3>
            {analysis && (
              <span className={`text-xs px-2 py-0.5 rounded ${
                analysis.recommendation === 'strong_buy' || analysis.recommendation === 'buy'
                  ? 'bg-green-500/20 text-green-400'
                  : analysis.recommendation === 'strong_sell' || analysis.recommendation === 'sell'
                  ? 'bg-red-500/20 text-red-400'
                  : 'bg-slate-500/20 text-slate-400'
              }`}>
                {analysis.recommendation.replace('_', ' ').toUpperCase()}
              </span>
            )}
          </div>
          <p className="text-xs text-slate-400 line-clamp-2">{market.title}</p>
        </div>
        
        {analysis && (
          <div className="flex items-center gap-1 ml-4">
            {isPositiveEdge ? (
              <TrendingUp className="w-4 h-4 text-green-400" />
            ) : (
              <TrendingDown className="w-4 h-4 text-red-400" />
            )}
            <span className={`text-sm font-bold ${
              Math.abs(edge) > 10 
                ? isPositiveEdge ? 'text-green-400' : 'text-red-400'
                : 'text-slate-400'
            }`}>
              {edge > 0 ? '+' : ''}{edge.toFixed(1)}%
            </span>
          </div>
        )}
      </div>

      <div className="grid grid-cols-4 gap-3 text-xs">
        <div>
          <p className="text-slate-500 mb-1">YES Price</p>
          <p className="font-semibold text-green-400">${market.yes_price.toFixed(2)}</p>
        </div>
        <div>
          <p className="text-slate-500 mb-1">NO Price</p>
          <p className="font-semibold text-red-400">${market.no_price.toFixed(2)}</p>
        </div>
        <div>
          <p className="text-slate-500 mb-1">Volume</p>
          <p className="font-semibold">{(market.volume / 1000).toFixed(1)}K</p>
        </div>
        <div>
          <p className="text-slate-500 mb-1">Liquidity</p>
          <p className="font-semibold">${(market.liquidity / 1000).toFixed(1)}K</p>
        </div>
      </div>

      {analysis && (
        <div className="mt-3 pt-3 border-t border-slate-600">
          <div className="flex items-center justify-between text-xs">
            <div className="flex items-center gap-4">
              <span className="text-slate-400">
                Confidence: <span className="text-white font-semibold">{analysis.confidence_score.toFixed(0)}%</span>
              </span>
              <span className="text-slate-400">
                Risk: <span className={`font-semibold ${
                  analysis.risk_level === 'low' ? 'text-green-400' :
                  analysis.risk_level === 'medium' ? 'text-yellow-400' : 'text-red-400'
                }`}>{analysis.risk_level.toUpperCase()}</span>
              </span>
            </div>
            
            {analysis.recommended_side && (
              <span className={`px-2 py-1 rounded text-xs font-semibold ${
                analysis.recommended_side === 'yes'
                  ? 'bg-green-500/20 text-green-400'
                  : 'bg-red-500/20 text-red-400'
              }`}>
                Recommended: {analysis.recommended_side.toUpperCase()} {analysis.recommended_size?.toFixed(1)}%
              </span>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
