import { kalshiAPI, Market, TradeOrder, Position, Balance } from './kalshi-api';
import { marketAnalyzer, MarketAnalysis } from './market-analyzer';
import { riskManager, RiskAssessment } from './risk-manager';

export interface TradingConfig {
  autoTradeEnabled: boolean;
  minEdgeThreshold: number;
  minConfidenceThreshold: number;
  scanIntervalSeconds: number;
  maxPositions: number;
  requireManualApproval: boolean;
}

export interface TradeExecution {
  market_id: string;
  ticker: string;
  side: 'yes' | 'no';
  quantity: number;
  price: number;
  analysis: MarketAnalysis;
  riskAssessment: RiskAssessment;
  timestamp: number;
  status: 'pending' | 'approved' | 'executed' | 'rejected' | 'failed';
  reason?: string;
}

export interface TradingSignal {
  market: Market;
  analysis: MarketAnalysis;
  action: 'buy' | 'sell' | 'hold';
  side?: 'yes' | 'no';
  size: number;
  confidence: number;
  urgency: number;
}

export class TradingEngine {
  private config: TradingConfig;
  private isRunning: boolean = false;
  private scanInterval: NodeJS.Timeout | null = null;
  private executionHistory: TradeExecution[] = [];
  private pendingApprovals: TradeExecution[] = [];
  
  constructor(customConfig?: Partial<TradingConfig>) {
    this.config = {
      autoTradeEnabled: false,
      minEdgeThreshold: 8,
      minConfidenceThreshold: 50,
      scanIntervalSeconds: 60,
      maxPositions: 10,
      requireManualApproval: true,
      ...customConfig,
    };
  }

  /**
   * Start the trading engine
   */
  async start(): Promise<void> {
    if (this.isRunning) {
      console.log('Trading engine already running');
      return;
    }

    if (!kalshiAPI.isAuthenticated()) {
      throw new Error('Not authenticated with Kalshi API');
    }

    this.isRunning = true;
    console.log('Trading engine started');
    
    // Run initial scan
    await this.scanMarkets();
    
    // Set up periodic scanning
    this.scanInterval = setInterval(
      () => this.scanMarkets(),
      this.config.scanIntervalSeconds * 1000
    );
  }

  /**
   * Stop the trading engine
   */
  stop(): void {
    if (this.scanInterval) {
      clearInterval(this.scanInterval);
      this.scanInterval = null;
    }
    this.isRunning = false;
    console.log('Trading engine stopped');
  }

  /**
   * Scan markets for trading opportunities
   */
  async scanMarkets(): Promise<TradingSignal[]> {
    try {
      console.log('Scanning markets...');
      
      // Fetch active markets
      const markets = await kalshiAPI.getMarkets({
        status: 'open',
        limit: 100,
      });

      if (markets.length === 0) {
        console.log('No active markets found');
        return [];
      }

      // Analyze all markets
      const analyses = await marketAnalyzer.analyzeMultipleMarkets(markets);
      
      // Find trading opportunities
      const signals = this.generateTradingSignals(analyses, markets);
      
      console.log(`Found ${signals.length} trading signals`);
      
      // Execute trades if auto-trading is enabled
      if (this.config.autoTradeEnabled && signals.length > 0) {
        await this.executeSignals(signals);
      }
      
      return signals;
    } catch (error) {
      console.error('Error scanning markets:', error);
      return [];
    }
  }

  /**
   * Generate trading signals from market analyses
   */
  private generateTradingSignals(
    analyses: MarketAnalysis[],
    markets: Market[]
  ): TradingSignal[] {
    const signals: TradingSignal[] = [];

    for (const analysis of analyses) {
      // Skip if no clear recommendation
      if (analysis.recommendation === 'hold') continue;
      
      // Skip if below thresholds
      if (Math.abs(analysis.edge_score) < this.config.minEdgeThreshold) continue;
      if (analysis.confidence_score < this.config.minConfidenceThreshold) continue;
      
      const market = markets.find(m => m.id === analysis.market_id);
      if (!market) continue;

      const action: 'buy' | 'sell' = 
        analysis.recommendation === 'strong_buy' || analysis.recommendation === 'buy'
          ? 'buy'
          : 'sell';

      signals.push({
        market,
        analysis,
        action,
        side: analysis.recommended_side,
        size: analysis.recommended_size || 0,
        confidence: analysis.confidence_score,
        urgency: analysis.urgency_score,
      });
    }

    // Sort by score (edge * confidence)
    return signals.sort((a, b) => {
      const scoreA = Math.abs(a.analysis.edge_score) * a.confidence;
      const scoreB = Math.abs(b.analysis.edge_score) * b.confidence;
      return scoreB - scoreA;
    });
  }

  /**
   * Execute trading signals
   */
  private async executeSignals(signals: TradingSignal[]): Promise<void> {
    // Get current portfolio state
    const balance = await kalshiAPI.getBalance();
    const positions = await kalshiAPI.getPositions();
    
    if (!balance) {
      console.error('Failed to fetch balance');
      return;
    }

    // Limit to max positions
    const remainingSlots = this.config.maxPositions - positions.length;
    const signalsToExecute = signals.slice(0, remainingSlots);

    for (const signal of signalsToExecute) {
      await this.executeTrade(signal, balance, positions);
    }
  }

  /**
   * Execute a single trade
   */
  async executeTrade(
    signal: TradingSignal,
    balance: Balance,
    positions: Position[]
  ): Promise<TradeExecution> {
    const execution: TradeExecution = {
      market_id: signal.market.id,
      ticker: signal.market.ticker,
      side: signal.side!,
      quantity: 0,
      price: signal.side === 'yes' ? signal.market.yes_price : signal.market.no_price,
      analysis: signal.analysis,
      riskAssessment: { approved: false, warnings: [] },
      timestamp: Date.now(),
      status: 'pending',
    };

    try {
      // Risk assessment
      const riskAssessment = await riskManager.assessTrade(
        signal.analysis,
        balance,
        positions
      );
      
      execution.riskAssessment = riskAssessment;

      if (!riskAssessment.approved) {
        execution.status = 'rejected';
        execution.reason = riskAssessment.reason;
        this.executionHistory.push(execution);
        console.log(`Trade rejected: ${execution.reason}`);
        return execution;
      }

      // Calculate quantity based on adjusted size
      const positionValue = (balance.balance * (riskAssessment.adjustedSize || 0)) / 100;
      const quantity = Math.floor(positionValue / execution.price);
      execution.quantity = quantity;

      if (quantity < 1) {
        execution.status = 'rejected';
        execution.reason = 'Position size too small';
        this.executionHistory.push(execution);
        return execution;
      }

      // Check if manual approval required
      if (this.config.requireManualApproval) {
        execution.status = 'approved';
        this.pendingApprovals.push(execution);
        console.log(`Trade pending approval: ${signal.market.ticker} ${signal.side} x${quantity}`);
        return execution;
      }

      // Execute trade
      const order: TradeOrder = {
        market_id: signal.market.id,
        side: signal.side!,
        action: signal.action,
        quantity,
        type: 'market',
      };

      const success = await kalshiAPI.placeTrade(order);
      
      if (success) {
        execution.status = 'executed';
        console.log(`✅ Trade executed: ${signal.market.ticker} ${signal.side} x${quantity} @ ${execution.price}`);
      } else {
        execution.status = 'failed';
        execution.reason = 'API order placement failed';
        console.log(`❌ Trade failed: ${signal.market.ticker}`);
      }

      this.executionHistory.push(execution);
      return execution;

    } catch (error) {
      execution.status = 'failed';
      execution.reason = error instanceof Error ? error.message : 'Unknown error';
      this.executionHistory.push(execution);
      console.error('Trade execution error:', error);
      return execution;
    }
  }

  /**
   * Approve a pending trade
   */
  async approveTrade(executionId: string): Promise<boolean> {
    const idx = this.pendingApprovals.findIndex(e => 
      `${e.market_id}-${e.timestamp}` === executionId
    );
    
    if (idx === -1) return false;
    
    const execution = this.pendingApprovals[idx];
    this.pendingApprovals.splice(idx, 1);

    const order: TradeOrder = {
      market_id: execution.market_id,
      side: execution.side,
      action: 'buy',
      quantity: execution.quantity,
      type: 'market',
    };

    const success = await kalshiAPI.placeTrade(order);
    
    if (success) {
      execution.status = 'executed';
    } else {
      execution.status = 'failed';
      execution.reason = 'Order placement failed';
    }

    this.executionHistory.push(execution);
    return success;
  }

  /**
   * Reject a pending trade
   */
  rejectTrade(executionId: string): boolean {
    const idx = this.pendingApprovals.findIndex(e => 
      `${e.market_id}-${e.timestamp}` === executionId
    );
    
    if (idx === -1) return false;
    
    const execution = this.pendingApprovals[idx];
    execution.status = 'rejected';
    execution.reason = 'Manually rejected';
    
    this.pendingApprovals.splice(idx, 1);
    this.executionHistory.push(execution);
    
    return true;
  }

  /**
   * Monitor existing positions for exit signals
   */
  async monitorPositions(): Promise<void> {
    const positions = await kalshiAPI.getPositions();
    const balance = await kalshiAPI.getBalance();
    
    if (!balance) return;

    for (const position of positions) {
      const market = await kalshiAPI.getMarket(position.market_id);
      if (!market) continue;

      const currentPrice = position.side === 'yes' ? market.yes_price : market.no_price;
      
      // Check risk-based exit
      const riskCheck = riskManager.shouldClosePosition(position, currentPrice);
      
      if (riskCheck.shouldClose) {
        console.log(`Closing position ${market.ticker}: ${riskCheck.reason}`);
        await this.closePosition(position, market);
        continue;
      }

      // Check for profit-taking opportunities
      const analysis = await marketAnalyzer.analyzeMarket(market);
      
      if (analysis.recommendation === 'sell' || analysis.recommendation === 'strong_sell') {
        console.log(`Taking profit on ${market.ticker}`);
        await this.closePosition(position, market);
      }
    }
  }

  /**
   * Close a position
   */
  private async closePosition(position: Position, market: Market): Promise<boolean> {
    const order: TradeOrder = {
      market_id: position.market_id,
      side: position.side,
      action: 'sell',
      quantity: Math.abs(position.position),
      type: 'market',
    };

    return await kalshiAPI.placeTrade(order);
  }

  /**
   * Get pending approvals
   */
  getPendingApprovals(): TradeExecution[] {
    return [...this.pendingApprovals];
  }

  /**
   * Get execution history
   */
  getExecutionHistory(limit?: number): TradeExecution[] {
    const history = [...this.executionHistory].reverse();
    return limit ? history.slice(0, limit) : history;
  }

  /**
   * Get trading statistics
   */
  getStatistics(): {
    totalTrades: number;
    successRate: number;
    totalProfit: number;
    averageReturn: number;
  } {
    const executed = this.executionHistory.filter(e => e.status === 'executed');
    
    return {
      totalTrades: executed.length,
      successRate: executed.length > 0 
        ? (executed.filter(e => e.analysis.edge_score > 0).length / executed.length) * 100 
        : 0,
      totalProfit: 0, // Would need position tracking
      averageReturn: 0, // Would need position tracking
    };
  }

  /**
   * Update configuration
   */
  updateConfig(newConfig: Partial<TradingConfig>): void {
    this.config = { ...this.config, ...newConfig };
    
    // Restart if scan interval changed
    if (newConfig.scanIntervalSeconds && this.isRunning) {
      this.stop();
      this.start();
    }
  }

  /**
   * Get current configuration
   */
  getConfig(): TradingConfig {
    return { ...this.config };
  }

  /**
   * Check if engine is running
   */
  isEngineRunning(): boolean {
    return this.isRunning;
  }
}

export const tradingEngine = new TradingEngine();
