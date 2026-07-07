import { Market } from './kalshi-api';

export interface MarketAnalysis {
  market_id: string;
  ticker: string;
  title: string;
  
  // Price Analysis
  fair_value: number;
  implied_probability: number;
  edge_score: number; // -100 to +100, negative = no edge, positive = edge
  
  // Value Assessment
  is_undervalued: boolean;
  is_overvalued: boolean;
  value_score: number;
  
  // Statistical Metrics
  volume_score: number;
  liquidity_score: number;
  volatility: number;
  momentum: number;
  
  // Risk Assessment
  risk_level: 'low' | 'medium' | 'high';
  confidence_score: number; // 0-100
  
  // Trading Recommendation
  recommendation: 'strong_buy' | 'buy' | 'hold' | 'sell' | 'strong_sell';
  recommended_side?: 'yes' | 'no';
  recommended_size?: number;
  
  // Timing
  time_decay_factor: number;
  urgency_score: number;
  
  // Additional Insights
  insights: string[];
  warnings: string[];
}

export class MarketAnalyzer {
  
  /**
   * Comprehensive market analysis combining multiple strategies
   */
  async analyzeMarket(market: Market, historicalData?: any[]): Promise<MarketAnalysis> {
    const impliedProb = this.calculateImpliedProbability(market);
    const fairValue = this.estimateFairValue(market, historicalData);
    const edge = this.calculateEdge(impliedProb, fairValue);
    
    const volumeScore = this.calculateVolumeScore(market);
    const liquidityScore = this.calculateLiquidityScore(market);
    const volatility = this.calculateVolatility(historicalData);
    const momentum = this.calculateMomentum(historicalData);
    
    const riskLevel = this.assessRiskLevel(market, volatility);
    const confidenceScore = this.calculateConfidence(
      liquidityScore,
      volumeScore,
      historicalData?.length || 0
    );
    
    const timeDecay = this.calculateTimeDecay(market);
    const urgency = this.calculateUrgency(market, edge, timeDecay);
    
    const { recommendation, side, size } = this.generateRecommendation(
      edge,
      confidenceScore,
      riskLevel,
      liquidityScore,
      impliedProb
    );
    
    const insights = this.generateInsights(market, edge, momentum, volatility);
    const warnings = this.generateWarnings(market, riskLevel, liquidityScore);
    
    return {
      market_id: market.id,
      ticker: market.ticker,
      title: market.title,
      fair_value: fairValue,
      implied_probability: impliedProb,
      edge_score: edge,
      is_undervalued: edge > 5,
      is_overvalued: edge < -5,
      value_score: edge,
      volume_score: volumeScore,
      liquidity_score: liquidityScore,
      volatility,
      momentum,
      risk_level: riskLevel,
      confidence_score: confidenceScore,
      recommendation,
      recommended_side: side,
      recommended_size: size,
      time_decay_factor: timeDecay,
      urgency_score: urgency,
      insights,
      warnings,
    };
  }

  /**
   * Calculate implied probability from market prices
   */
  private calculateImpliedProbability(market: Market): number {
    return market.yes_price;
  }

  /**
   * Estimate fair value using multiple models
   */
  private estimateFairValue(market: Market, history?: any[]): number {
    // Base fair value on multiple factors
    let fairValue = market.yes_price;
    
    // Adjust based on volume-weighted average
    if (history && history.length > 0) {
      const recentPrices = history.slice(-20);
      const vwap = recentPrices.reduce((acc, h) => acc + h.price * h.volume, 0) / 
                   recentPrices.reduce((acc, h) => acc + h.volume, 1);
      fairValue = (fairValue * 0.6 + vwap * 0.4);
    }
    
    // Adjust for time decay (markets closer to resolution are more certain)
    const timeAdjustment = this.calculateTimeDecay(market);
    fairValue = fairValue * (1 - timeAdjustment * 0.1);
    
    return Math.max(0.01, Math.min(0.99, fairValue));
  }

  /**
   * Calculate edge: difference between fair value and market price
   */
  private calculateEdge(impliedProb: number, fairValue: number): number {
    return ((fairValue - impliedProb) / impliedProb) * 100;
  }

  /**
   * Calculate volume score (higher = more liquid market)
   */
  private calculateVolumeScore(market: Market): number {
    // Normalize volume to 0-100 scale
    const normalizedVolume = Math.min(100, (market.volume / 10000) * 100);
    return normalizedVolume;
  }

  /**
   * Calculate liquidity score
   */
  private calculateLiquidityScore(market: Market): number {
    const liquidity = market.liquidity || 0;
    return Math.min(100, (liquidity / 5000) * 100);
  }

  /**
   * Calculate price volatility from historical data
   */
  private calculateVolatility(history?: any[]): number {
    if (!history || history.length < 2) return 50;
    
    const prices = history.slice(-30).map(h => h.price);
    const mean = prices.reduce((a, b) => a + b, 0) / prices.length;
    const variance = prices.reduce((acc, price) => acc + Math.pow(price - mean, 2), 0) / prices.length;
    const stdDev = Math.sqrt(variance);
    
    return Math.min(100, stdDev * 500);
  }

  /**
   * Calculate price momentum
   */
  private calculateMomentum(history?: any[]): number {
    if (!history || history.length < 2) return 0;
    
    const recent = history.slice(-10);
    const older = history.slice(-20, -10);
    
    const recentAvg = recent.reduce((acc, h) => acc + h.price, 0) / recent.length;
    const olderAvg = older.reduce((acc, h) => acc + h.price, 0) / (older.length || 1);
    
    return ((recentAvg - olderAvg) / olderAvg) * 100;
  }

  /**
   * Assess risk level
   */
  private assessRiskLevel(market: Market, volatility: number): 'low' | 'medium' | 'high' {
    if (volatility > 70 || market.liquidity < 1000) return 'high';
    if (volatility > 40 || market.liquidity < 3000) return 'medium';
    return 'low';
  }

  /**
   * Calculate confidence in analysis
   */
  private calculateConfidence(liquidityScore: number, volumeScore: number, dataPoints: number): number {
    const liquidityWeight = liquidityScore * 0.4;
    const volumeWeight = volumeScore * 0.3;
    const dataWeight = Math.min(30, dataPoints / 10) * 1;
    
    return Math.min(100, liquidityWeight + volumeWeight + dataWeight);
  }

  /**
   * Calculate time decay factor
   */
  private calculateTimeDecay(market: Market): number {
    const now = Date.now();
    const closeTime = new Date(market.close_time).getTime();
    const timeRemaining = closeTime - now;
    const hoursRemaining = timeRemaining / (1000 * 60 * 60);
    
    if (hoursRemaining < 0) return 1;
    if (hoursRemaining < 24) return 0.8;
    if (hoursRemaining < 168) return 0.5; // 1 week
    return 0.2;
  }

  /**
   * Calculate urgency score for trading
   */
  private calculateUrgency(market: Market, edge: number, timeDecay: number): number {
    const edgeUrgency = Math.abs(edge) * 0.5;
    const timeUrgency = timeDecay * 50;
    
    return Math.min(100, edgeUrgency + timeUrgency);
  }

  /**
   * Generate trading recommendation
   */
  private generateRecommendation(
    edge: number,
    confidence: number,
    riskLevel: string,
    liquidity: number,
    impliedProb: number
  ): { recommendation: MarketAnalysis['recommendation']; side?: 'yes' | 'no'; size?: number } {
    
    // Don't trade if confidence or liquidity is too low
    if (confidence < 30 || liquidity < 20) {
      return { recommendation: 'hold' };
    }
    
    const adjustedEdge = edge * (confidence / 100);
    
    // Determine position side
    const side: 'yes' | 'no' = edge > 0 ? 'yes' : 'no';
    
    // Calculate position size (as percentage of bankroll)
    const kellyFraction = Math.abs(adjustedEdge) / 100;
    const conservativeSize = kellyFraction * 0.25; // Quarter Kelly for safety
    const size = Math.max(1, Math.min(10, conservativeSize * 100));
    
    if (adjustedEdge > 15 && confidence > 70) {
      return { recommendation: 'strong_buy', side, size };
    } else if (adjustedEdge > 8 && confidence > 50) {
      return { recommendation: 'buy', side, size: size * 0.7 };
    } else if (adjustedEdge < -15 && confidence > 70) {
      return { recommendation: 'strong_sell', side, size };
    } else if (adjustedEdge < -8 && confidence > 50) {
      return { recommendation: 'sell', side, size: size * 0.7 };
    }
    
    return { recommendation: 'hold' };
  }

  /**
   * Generate insights
   */
  private generateInsights(market: Market, edge: number, momentum: number, volatility: number): string[] {
    const insights: string[] = [];
    
    if (Math.abs(edge) > 10) {
      insights.push(`Strong ${edge > 0 ? 'YES' : 'NO'} edge detected (${edge.toFixed(1)}%)`);
    }
    
    if (momentum > 5) {
      insights.push(`Positive momentum: Price trending upward`);
    } else if (momentum < -5) {
      insights.push(`Negative momentum: Price trending downward`);
    }
    
    if (volatility > 60) {
      insights.push(`High volatility detected - expect price swings`);
    }
    
    if (market.volume > 50000) {
      insights.push(`High trading volume indicates strong market interest`);
    }
    
    return insights;
  }

  /**
   * Generate warnings
   */
  private generateWarnings(market: Market, riskLevel: string, liquidity: number): string[] {
    const warnings: string[] = [];
    
    if (riskLevel === 'high') {
      warnings.push(`High risk market - trade with caution`);
    }
    
    if (liquidity < 30) {
      warnings.push(`Low liquidity - may be difficult to exit position`);
    }
    
    if (market.volume < 1000) {
      warnings.push(`Low volume - limited price discovery`);
    }
    
    const hoursToClose = (new Date(market.close_time).getTime() - Date.now()) / (1000 * 60 * 60);
    if (hoursToClose < 24) {
      warnings.push(`Market closes in ${hoursToClose.toFixed(0)} hours`);
    }
    
    return warnings;
  }

  /**
   * Batch analyze multiple markets
   */
  async analyzeMultipleMarkets(markets: Market[]): Promise<MarketAnalysis[]> {
    const analyses = await Promise.all(
      markets.map(market => this.analyzeMarket(market))
    );
    
    return analyses.sort((a, b) => {
      const scoreA = Math.abs(a.edge_score) * (a.confidence_score / 100);
      const scoreB = Math.abs(b.edge_score) * (b.confidence_score / 100);
      return scoreB - scoreA;
    });
  }

  /**
   * Find best opportunities across all markets
   */
  findBestOpportunities(analyses: MarketAnalysis[], minConfidence: number = 50): MarketAnalysis[] {
    return analyses.filter(a => 
      (a.recommendation === 'strong_buy' || a.recommendation === 'buy') &&
      a.confidence_score >= minConfidence &&
      a.liquidity_score >= 30
    );
  }
}

export const marketAnalyzer = new MarketAnalyzer();
