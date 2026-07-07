import { create } from 'zustand';
import { Market, Position, Balance, KalshiCredentials } from './kalshi-api';
import { MarketAnalysis } from './market-analyzer';
import { TradingSignal, TradeExecution } from './trading-engine';
import { PortfolioRisk } from './risk-manager';

interface AppState {
  // Authentication
  isAuthenticated: boolean;
  credentials: KalshiCredentials | null;
  
  // Market Data
  markets: Market[];
  analyses: MarketAnalysis[];
  selectedMarket: Market | null;
  
  // Portfolio
  balance: Balance | null;
  positions: Position[];
  portfolioRisk: PortfolioRisk | null;
  
  // Trading
  tradingSignals: TradingSignal[];
  pendingApprovals: TradeExecution[];
  executionHistory: TradeExecution[];
  isAutoTrading: boolean;
  
  // UI State
  isLoading: boolean;
  error: string | null;
  lastUpdate: number;
  
  // Actions
  setAuthenticated: (value: boolean) => void;
  setCredentials: (credentials: KalshiCredentials | null) => void;
  setMarkets: (markets: Market[]) => void;
  setAnalyses: (analyses: MarketAnalysis[]) => void;
  setSelectedMarket: (market: Market | null) => void;
  setBalance: (balance: Balance | null) => void;
  setPositions: (positions: Position[]) => void;
  setPortfolioRisk: (risk: PortfolioRisk | null) => void;
  setTradingSignals: (signals: TradingSignal[]) => void;
  setPendingApprovals: (approvals: TradeExecution[]) => void;
  setExecutionHistory: (history: TradeExecution[]) => void;
  setAutoTrading: (enabled: boolean) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  updateLastUpdate: () => void;
  reset: () => void;
}

export const useStore = create<AppState>((set) => ({
  // Initial State
  isAuthenticated: false,
  credentials: null,
  markets: [],
  analyses: [],
  selectedMarket: null,
  balance: null,
  positions: [],
  portfolioRisk: null,
  tradingSignals: [],
  pendingApprovals: [],
  executionHistory: [],
  isAutoTrading: false,
  isLoading: false,
  error: null,
  lastUpdate: Date.now(),
  
  // Actions
  setAuthenticated: (value) => set({ isAuthenticated: value }),
  setCredentials: (credentials) => set({ credentials }),
  setMarkets: (markets) => set({ markets, lastUpdate: Date.now() }),
  setAnalyses: (analyses) => set({ analyses, lastUpdate: Date.now() }),
  setSelectedMarket: (market) => set({ selectedMarket: market }),
  setBalance: (balance) => set({ balance, lastUpdate: Date.now() }),
  setPositions: (positions) => set({ positions, lastUpdate: Date.now() }),
  setPortfolioRisk: (risk) => set({ portfolioRisk: risk }),
  setTradingSignals: (signals) => set({ tradingSignals: signals, lastUpdate: Date.now() }),
  setPendingApprovals: (approvals) => set({ pendingApprovals: approvals }),
  setExecutionHistory: (history) => set({ executionHistory: history }),
  setAutoTrading: (enabled) => set({ isAutoTrading: enabled }),
  setLoading: (loading) => set({ isLoading: loading }),
  setError: (error) => set({ error }),
  updateLastUpdate: () => set({ lastUpdate: Date.now() }),
  reset: () => set({
    isAuthenticated: false,
    credentials: null,
    markets: [],
    analyses: [],
    selectedMarket: null,
    balance: null,
    positions: [],
    portfolioRisk: null,
    tradingSignals: [],
    pendingApprovals: [],
    executionHistory: [],
    isAutoTrading: false,
    isLoading: false,
    error: null,
    lastUpdate: Date.now(),
  }),
}));
