import { PublicMarket } from './kalshi-public-api';

export interface BettingRecommendation {
  ticker: string;
  title: string;
  category: string;
  
  // Recommendation
  recommendation: 'STRONG BUY' | 'BUY' | 'HOLD' | 'AVOID';
  recommended_side: 'YES' | 'NO';
  
  // Pricing
  current_price: number;
  fair_value_estimate: number;
  edge_percentage: number;
  
  // Market metrics
  volume_24h: number;
  liquidity: number;
  spread: number;
  
  // Confidence & Risk
  confidence_score: number; // 0-100
  risk_level: 'LOW' | 'MEDIUM' | 'HIGH';
  
  // Timing
  closes_in_hours: number;
  urgency: 'LOW' | 'MEDIUM' | 'HIGH';
  
  // Insights
  reasons: string[];
  warnings: string[];
}

export class PublicMarketAnalyzer {
  
  /**
   * Analyze a single market and generate betting recommendation
   */
  analyzeMarket(market: PublicMarket): BettingRecommendation {
    // Calculate current effective price (midpoint of bid/ask)
    const yesPrice = (market.yes_bid + market.yes_ask) / 2;
    const noPrice = (market.no_bid + market.no_ask) / 2;
    
    // Calculate spread (tighter = better liquidity)
    const spread = market.yes_ask - market.yes_bid;
    
    // Estimate fair value based on multiple factors
    const fairValue = this.estimateFairValue(market);
    
    // Calculate edge for YES and NO
    const yesEdge = ((fairValue - yesPrice) / yesPrice) * 100;
    const noEdge = (((1 - fairValue) - noPrice) / noPrice) * 100;
    
    // Determine which side has better edge
    const bestSide = Math.abs(yesEdge) > Math.abs(noEdge) ? 'YES' : 'NO';
    const bestEdge = bestSide === 'YES' ? yesEdge : noEdge;
    const bestPrice = bestSide === 'YES' ? yesPrice : noPrice;
    
    // Calculate confidence based on data quality
    const confidence = this.calculateConfidence(market, spread);
    
    // Assess risk level
    const riskLevel = this.assessRiskLevel(market, spread);
    
    // Generate recommendation
    const recommendation = this.generateRecommendation(bestEdge, confidence, riskLevel);
    
    // Calculate time to close
    const closesInHours = this.getHoursUntilClose(market.close_time);
    const urgency = this.calculateUrgency(closesInHours, bestEdge);
    
    // Generate insights and warnings
    const reasons = this.generateReasons(bestEdge, market, bestSide);
    const warnings = this.generateWarnings(market, riskLevel, spread);
    
    return {
      ticker: market.ticker,
      title: market.title,
      category: market.category,
      recommendation,
      recommended_side: bestSide,
      current_price: bestPrice,
      fair_value_estimate: bestSide === 'YES' ? fairValue : (1 - fairValue),
      edge_percentage: bestEdge,
      volume_24h: market.volume_24h,
      liquidity: market.liquidity,
      spread,
      confidence_score: confidence,
      risk_level: riskLevel,
      closes_in_hours: closesInHours,
      urgency,
      reasons,
      warnings,
    };
  }

  /**
   * Estimate fair value using volume-weighted price and market dynamics
   */
  private estimateFairValue(market: PublicMarket): number {
    let fairValue = market.last_price;
    
    // Adjust based on bid/ask midpoint
    const midpoint = (market.yes_bid + market.yes_ask) / 2;
    fairValue = (fairValue * 0.6 + midpoint * 0.4);
    
    // Adjust for momentum (if price is moving)
    const priceChange = market.last_price - market.previous_price;
    const momentum = priceChange / (market.previous_price || 1);
    fairValue += momentum * 0.1;
    
    return Math.max(0.01, Math.min(0.99, fairValue));
  }

  /**
   * Calculate confidence score based on data quality
   */
  private calculateConfidence(market: PublicMarket, spread: number): number {
    let confidence = 50;
    
    // Higher volume = higher confidence
    if (market.volume_24h > 10000) confidence += 20;
    else if (market.volume_24h > 5000) confidence += 10;
    else if (market.volume_24h > 1000) confidence += 5;
    
    // Higher liquidity = higher confidence
    if (market.liquidity > 5000) confidence += 15;
    else if (market.liquidity > 2000) confidence += 10;
    else if (market.liquidity > 500) confidence += 5;
    
    // Tighter spread = higher confidence
    if (spread < 0.02) confidence += 15;
    else if (spread < 0.05) confidence += 10;
    else if (spread < 0.10) confidence += 5;
    
    return Math.min(100, confidence);
  }

  /**
   * Assess risk level based on market characteristics
   */
  private assessRiskLevel(market: PublicMarket, spread: number): 'LOW' | 'MEDIUM' | 'HIGH' {
    let riskScore = 0;
    
    if (spread > 0.15) riskScore += 3;
    else if (spread > 0.10) riskScore += 2;
    else if (spread > 0.05) riskScore += 1;
    
    if (market.liquidity < 1000) riskScore += 3;
    else if (market.liquidity < 3000) riskScore += 2;
    else if (market.liquidity < 5000) riskScore += 1;
    
    if (market.volume_24h < 500) riskScore += 2;
    else if (market.volume_24h < 2000) riskScore += 1;
    
    if (riskScore >= 5) return 'HIGH';
    if (riskScore >= 3) return 'MEDIUM';
    return 'LOW';
  }

  /**
   * Generate trading recommendation
   */
  private generateRecommendation(
    edge: number,
    confidence: number,
    riskLevel: string
  ): 'STRONG BUY' | 'BUY' | 'HOLD' | 'AVOID' {
    const adjustedEdge = edge * (confidence / 100);
    
    if (riskLevel === 'HIGH' && adjustedEdge < 15) return 'AVOID';
    
    if (adjustedEdge > 15 && confidence > 70) return 'STRONG BUY';
    if (adjustedEdge > 8 && confidence > 50) return 'BUY';
    if (adjustedEdge < -10) return 'AVOID';
    
    return 'HOLD';
  }

  /**
   * Calculate hours until market closes
   */
  private getHoursUntilClose(closeTime: string): number {
    const close = new Date(closeTime).getTime();
    const now = Date.now();
    return Math.max(0, (close - now) / (1000 * 60 * 60));
  }

  /**
   * Calculate urgency level
   */
  private calculateUrgency(hours: number, edge: number): 'LOW' | 'MEDIUM' | 'HIGH' {
    if (hours < 24 && Math.abs(edge) > 10) return 'HIGH';
    if (hours < 72 && Math.abs(edge) > 8) return 'MEDIUM';
    return 'LOW';
  }

  /**
   * Generate reasons for recommendation
   */
  private generateReasons(edge: number, market: PublicMarket, side: string): string[] {
    const reasons: string[] = [];
    
    if (Math.abs(edge) > 10) {
      reasons.push(`Strong ${edge > 0 ? 'value' : 'overpriced'}: ${edge.toFixed(1)}% edge detected`);
    }
    
    if (market.volume_24h > 10000) {
      reasons.push(`High trading activity: ${(market.volume_24h / 1000).toFixed(1)}K volume`);
    }
    
    if (market.liquidity > 5000) {
      reasons.push(`Good liquidity: $${(market.liquidity / 1000).toFixed(1)}K available`);
    }
    
    const spread = market.yes_ask - market.yes_bid;
    if (spread < 0.05) {
      reasons.push(`Tight spread: Only ${(spread * 100).toFixed(1)}¢ between bid/ask`);
    }
    
    if (market.last_price - market.previous_price > 0.05) {
      reasons.push('Positive momentum: Price trending up');
    }
    
    return reasons;
  }

  /**
   * Generate warnings
   */
  private generateWarnings(market: PublicMarket, riskLevel: string, spread: number): string[] {
    const warnings: string[] = [];
    
    if (riskLevel === 'HIGH') {
      warnings.push('⚠️ High risk market - proceed with caution');
    }
    
    if (spread > 0.15) {
      warnings.push(`Wide spread: ${(spread * 100).toFixed(1)}¢ bid-ask gap`);
    }
    
    if (market.liquidity < 1000) {
      warnings.push('Low liquidity - may be hard to exit');
    }
    
    if (market.volume_24h < 500) {
      warnings.push('Low trading volume - limited activity');
    }
    
    const hours = this.getHoursUntilClose(market.close_time);
    if (hours < 24) {
      warnings.push(`⏰ Closes in ${hours.toFixed(0)} hours`);
    }
    
    return warnings;
  }

  /**
   * Analyze all markets and return best opportunities
   */
  analyzeBestOpportunities(markets: PublicMarket[]): BettingRecommendation[] {
    const recommendations = markets
      .map(market => this.analyzeMarket(market))
      .filter(rec => rec.recommendation === 'STRONG BUY' || rec.recommendation === 'BUY')
      .sort((a, b) => {
        const scoreA = Math.abs(a.edge_percentage) * (a.confidence_score / 100);
        const scoreB = Math.abs(b.edge_percentage) * (b.confidence_score / 100);
        return scoreB - scoreA;
      });
    
    return recommendations;
  }

  /**
   * Group recommendations by category
   */
  groupByCategory(recommendations: BettingRecommendation[]): Map<string, BettingRecommendation[]> {
    const grouped = new Map<string, BettingRecommendation[]>();
    
    for (const rec of recommendations) {
      if (!grouped.has(rec.category)) {
        grouped.set(rec.category, []);
      }
      grouped.get(rec.category)!.push(rec);
    }
    
    return grouped;
  }
}

export const publicMarketAnalyzer = new PublicMarketAnalyzer();
