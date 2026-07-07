import { MarketAnalysis } from './market-analyzer';
import { Position, Balance } from './kalshi-api';

export interface RiskLimits {
  maxPositionSize: number; // Max % of portfolio per position
  maxTotalExposure: number; // Max % of portfolio in active positions
  maxLossPerTrade: number; // Max % loss per trade
  maxDailyLoss: number; // Max % daily loss before stopping
  minLiquidity: number; // Minimum liquidity score to trade
  minConfidence: number; // Minimum confidence score to trade
  maxConcurrentPositions: number; // Max number of open positions
}

export interface RiskAssessment {
  approved: boolean;
  reason?: string;
  adjustedSize?: number;
  warnings: string[];
}

export interface PortfolioRisk {
  totalExposure: number;
  positionCount: number;
  dailyPnL: number;
  totalPnL: number;
  riskScore: number;
  isOverExposed: boolean;
  canTrade: boolean;
  reasons: string[];
}

export class RiskManager {
  private limits: RiskLimits;
  private dailyTrades: Map<string, number> = new Map();
  private dailyStartTime: number = Date.now();
  
  constructor(customLimits?: Partial<RiskLimits>) {
    this.limits = {
      maxPositionSize: 5, // 5% per position
      maxTotalExposure: 30, // 30% total
      maxLossPerTrade: 2, // 2% max loss
      maxDailyLoss: 10, // 10% daily loss limit
      minLiquidity: 30,
      minConfidence: 50,
      maxConcurrentPositions: 10,
      ...customLimits,
    };
  }

  /**
   * Assess if a trade should be approved
   */
  async assessTrade(
    analysis: MarketAnalysis,
    balance: Balance,
    positions: Position[]
  ): Promise<RiskAssessment> {
    const warnings: string[] = [];
    
    // Check portfolio risk
    const portfolioRisk = this.calculatePortfolioRisk(balance, positions);
    
    if (!portfolioRisk.canTrade) {
      return {
        approved: false,
        reason: portfolioRisk.reasons.join('; '),
        warnings,
      };
    }
    
    // Check confidence threshold
    if (analysis.confidence_score < this.limits.minConfidence) {
      return {
        approved: false,
        reason: `Confidence score ${analysis.confidence_score} below minimum ${this.limits.minConfidence}`,
        warnings,
      };
    }
    
    // Check liquidity threshold
    if (analysis.liquidity_score < this.limits.minLiquidity) {
      return {
        approved: false,
        reason: `Liquidity score ${analysis.liquidity_score} below minimum ${this.limits.minLiquidity}`,
        warnings,
      };
    }
    
    // Check position limits
    if (positions.length >= this.limits.maxConcurrentPositions) {
      return {
        approved: false,
        reason: `Maximum concurrent positions (${this.limits.maxConcurrentPositions}) reached`,
        warnings,
      };
    }
    
    // Calculate position size
    const recommendedSize = analysis.recommended_size || 0;
    const maxSize = this.calculateMaxPositionSize(balance, positions);
    const adjustedSize = Math.min(recommendedSize, maxSize);
    
    if (adjustedSize < 0.5) {
      return {
        approved: false,
        reason: 'Position size too small after risk adjustments',
        warnings,
      };
    }
    
    // Add warnings based on risk level
    if (analysis.risk_level === 'high') {
      warnings.push('High risk market - position size reduced by 50%');
    }
    
    if (portfolioRisk.riskScore > 70) {
      warnings.push('Portfolio risk elevated - consider reducing exposure');
    }
    
    if (analysis.urgency_score > 80) {
      warnings.push('High urgency trade - verify market conditions');
    }
    
    return {
      approved: true,
      adjustedSize: this.applyRiskAdjustments(adjustedSize, analysis, portfolioRisk),
      warnings,
    };
  }

  /**
   * Calculate maximum position size based on portfolio and limits
   */
  private calculateMaxPositionSize(balance: Balance, positions: Position[]): number {
    const availableBalance = balance.available_balance;
    const totalValue = balance.balance;
    
    // Calculate current exposure
    const currentExposure = positions.reduce((sum, p) => sum + Math.abs(p.total_cost), 0);
    const exposurePercent = (currentExposure / totalValue) * 100;
    
    // Calculate remaining capacity
    const remainingCapacity = Math.max(0, this.limits.maxTotalExposure - exposurePercent);
    const maxNewPositionPercent = Math.min(this.limits.maxPositionSize, remainingCapacity);
    
    return maxNewPositionPercent;
  }

  /**
   * Apply risk adjustments to position size
   */
  private applyRiskAdjustments(
    baseSize: number,
    analysis: MarketAnalysis,
    portfolioRisk: PortfolioRisk
  ): number {
    let adjustedSize = baseSize;
    
    // Reduce size for high-risk markets
    if (analysis.risk_level === 'high') {
      adjustedSize *= 0.5;
    } else if (analysis.risk_level === 'medium') {
      adjustedSize *= 0.75;
    }
    
    // Reduce size if portfolio risk is elevated
    if (portfolioRisk.riskScore > 70) {
      adjustedSize *= 0.7;
    } else if (portfolioRisk.riskScore > 50) {
      adjustedSize *= 0.85;
    }
    
    // Reduce size for lower confidence
    if (analysis.confidence_score < 70) {
      adjustedSize *= (analysis.confidence_score / 100);
    }
    
    // Ensure minimum viable size
    return Math.max(0.5, adjustedSize);
  }

  /**
   * Calculate overall portfolio risk
   */
  calculatePortfolioRisk(balance: Balance, positions: Position[]): PortfolioRisk {
    const totalValue = balance.balance;
    const currentExposure = positions.reduce((sum, p) => sum + Math.abs(p.total_cost), 0);
    const exposurePercent = (currentExposure / totalValue) * 100;
    
    const totalPnL = positions.reduce((sum, p) => sum + p.pnl, 0);
    const dailyPnL = this.calculateDailyPnL(positions);
    const dailyPnLPercent = (dailyPnL / totalValue) * 100;
    
    const reasons: string[] = [];
    let canTrade = true;
    
    // Check daily loss limit
    if (dailyPnLPercent < -this.limits.maxDailyLoss) {
      canTrade = false;
      reasons.push(`Daily loss limit exceeded: ${dailyPnLPercent.toFixed(2)}%`);
    }
    
    // Check total exposure limit
    const isOverExposed = exposurePercent >= this.limits.maxTotalExposure;
    if (isOverExposed) {
      canTrade = false;
      reasons.push(`Total exposure limit reached: ${exposurePercent.toFixed(2)}%`);
    }
    
    // Calculate risk score (0-100)
    const exposureRisk = (exposurePercent / this.limits.maxTotalExposure) * 40;
    const lossRisk = Math.abs(dailyPnLPercent / this.limits.maxDailyLoss) * 40;
    const concentrationRisk = (positions.length / this.limits.maxConcurrentPositions) * 20;
    const riskScore = Math.min(100, exposureRisk + lossRisk + concentrationRisk);
    
    return {
      totalExposure: exposurePercent,
      positionCount: positions.length,
      dailyPnL,
      totalPnL,
      riskScore,
      isOverExposed,
      canTrade,
      reasons,
    };
  }

  /**
   * Calculate daily P&L (simplified - would need trade history in production)
   */
  private calculateDailyPnL(positions: Position[]): number {
    // Reset daily tracking if new day
    const now = Date.now();
    if (now - this.dailyStartTime > 24 * 60 * 60 * 1000) {
      this.dailyStartTime = now;
      this.dailyTrades.clear();
    }
    
    // In production, this would track actual daily trades
    return positions.reduce((sum, p) => sum + p.pnl, 0);
  }

  /**
   * Calculate stop loss price for a position
   */
  calculateStopLoss(entryPrice: number, side: 'yes' | 'no'): number {
    const stopLossPercent = this.limits.maxLossPerTrade / 100;
    
    if (side === 'yes') {
      return Math.max(0.01, entryPrice * (1 - stopLossPercent));
    } else {
      return Math.min(0.99, entryPrice * (1 + stopLossPercent));
    }
  }

  /**
   * Calculate take profit price for a position
   */
  calculateTakeProfit(entryPrice: number, side: 'yes' | 'no', targetReturn: number = 0.20): number {
    if (side === 'yes') {
      return Math.min(0.99, entryPrice * (1 + targetReturn));
    } else {
      return Math.max(0.01, entryPrice * (1 - targetReturn));
    }
  }

  /**
   * Check if position should be closed based on risk rules
   */
  shouldClosePosition(position: Position, currentPrice: number): {
    shouldClose: boolean;
    reason?: string;
  } {
    const stopLoss = this.calculateStopLoss(position.average_price, position.side);
    
    // Check stop loss
    if (position.side === 'yes' && currentPrice <= stopLoss) {
      return { shouldClose: true, reason: 'Stop loss triggered' };
    }
    
    if (position.side === 'no' && currentPrice >= stopLoss) {
      return { shouldClose: true, reason: 'Stop loss triggered' };
    }
    
    // Check loss limit
    const lossPercent = (position.pnl / position.total_cost) * 100;
    if (lossPercent < -this.limits.maxLossPerTrade) {
      return { shouldClose: true, reason: 'Max loss per trade exceeded' };
    }
    
    return { shouldClose: false };
  }

  /**
   * Update risk limits
   */
  updateLimits(newLimits: Partial<RiskLimits>): void {
    this.limits = { ...this.limits, ...newLimits };
  }

  /**
   * Get current risk limits
   */
  getLimits(): RiskLimits {
    return { ...this.limits };
  }

  /**
   * Generate risk report
   */
  generateRiskReport(balance: Balance, positions: Position[]): string {
    const risk = this.calculatePortfolioRisk(balance, positions);
    
    return `
=== RISK REPORT ===
Portfolio Value: $${balance.balance.toFixed(2)}
Available Balance: $${balance.available_balance.toFixed(2)}

Exposure: ${risk.totalExposure.toFixed(2)}% (Limit: ${this.limits.maxTotalExposure}%)
Open Positions: ${risk.positionCount} (Limit: ${this.limits.maxConcurrentPositions})
Daily P&L: $${risk.dailyPnL.toFixed(2)} (${((risk.dailyPnL / balance.balance) * 100).toFixed(2)}%)
Total P&L: $${risk.totalPnL.toFixed(2)}

Risk Score: ${risk.riskScore.toFixed(0)}/100
Status: ${risk.canTrade ? 'CAN TRADE' : 'TRADING HALTED'}

${risk.reasons.length > 0 ? 'Warnings:\n' + risk.reasons.map(r => `- ${r}`).join('\n') : ''}
    `.trim();
  }
}

export const riskManager = new RiskManager();
