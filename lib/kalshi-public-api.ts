import axios, { AxiosInstance } from 'axios';

export interface PublicMarket {
  ticker: string;
  event_ticker: string;
  market_type: string;
  title: string;
  subtitle?: string;
  yes_sub_title: string;
  no_sub_title: string;
  yes_bid: number;
  yes_ask: number;
  no_bid: number;
  no_ask: number;
  last_price: number;
  previous_yes_bid: number;
  previous_yes_ask: number;
  previous_price: number;
  volume: number;
  volume_24h: number;
  liquidity: number;
  open_interest: number;
  close_time: string;
  expiration_time: string;
  expected_expiration_time: string;
  latest_expiration_time: string;
  status: string;
  can_close_early: boolean;
  category: string;
  strike_type?: string;
  floor_strike?: number;
  cap_strike?: number;
  custom_strike?: number;
}

export interface MarketResponse {
  markets: PublicMarket[];
  cursor?: string;
}

export class KalshiPublicAPI {
  private client: AxiosInstance;
  private baseURL = 'https://api.elections.kalshi.com/trade-api/v2';
  
  constructor() {
    this.client = axios.create({
      baseURL: this.baseURL,
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: 30000,
    });
  }

  /**
   * Fetch all available public markets
   */
  async getMarkets(params?: {
    limit?: number;
    cursor?: string;
    event_ticker?: string;
    series_ticker?: string;
    status?: 'open' | 'closed' | 'settled';
    tickers?: string;
  }): Promise<PublicMarket[]> {
    try {
      const response = await this.client.get<MarketResponse>('/markets', { 
        params: {
          limit: params?.limit || 200,
          status: params?.status || 'open',
          ...params
        }
      });
      return response.data.markets || [];
    } catch (error) {
      console.error('Failed to fetch markets:', error);
      return [];
    }
  }

  /**
   * Get a specific market by ticker
   */
  async getMarket(ticker: string): Promise<PublicMarket | null> {
    try {
      const response = await this.client.get(`/markets/${ticker}`);
      return response.data.market || null;
    } catch (error) {
      console.error('Failed to fetch market:', error);
      return null;
    }
  }

  /**
   * Get market history/trades
   */
  async getMarketHistory(ticker: string, params?: {
    limit?: number;
    cursor?: string;
    min_ts?: number;
    max_ts?: number;
  }): Promise<any[]> {
    try {
      const response = await this.client.get(`/markets/${ticker}/history`, { params });
      return response.data.history || [];
    } catch (error) {
      console.error('Failed to fetch market history:', error);
      return [];
    }
  }

  /**
   * Get all market categories
   */
  async getCategories(): Promise<string[]> {
    try {
      const markets = await this.getMarkets({ limit: 1000 });
      const categories = new Set(markets.map(m => m.category));
      return Array.from(categories).sort();
    } catch (error) {
      console.error('Failed to fetch categories:', error);
      return [];
    }
  }

  /**
   * Get markets by category
   */
  async getMarketsByCategory(category: string): Promise<PublicMarket[]> {
    try {
      const allMarkets = await this.getMarkets({ limit: 1000 });
      return allMarkets.filter(m => m.category === category);
    } catch (error) {
      console.error('Failed to fetch markets by category:', error);
      return [];
    }
  }
}

export const kalshiPublicAPI = new KalshiPublicAPI();
