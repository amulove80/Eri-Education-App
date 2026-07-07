import axios, { AxiosInstance } from 'axios';

export interface KalshiCredentials {
  email: string;
  password: string;
  apiKey?: string;
}

export interface Market {
  id: string;
  title: string;
  ticker: string;
  category: string;
  yes_price: number;
  no_price: number;
  volume: number;
  liquidity: number;
  close_time: string;
  open_time: string;
  status: string;
  result?: string;
  floor_price?: number;
  cap_price?: number;
}

export interface Position {
  market_id: string;
  position: number;
  side: 'yes' | 'no';
  average_price: number;
  total_cost: number;
  current_value: number;
  pnl: number;
}

export interface TradeOrder {
  market_id: string;
  side: 'yes' | 'no';
  action: 'buy' | 'sell';
  quantity: number;
  price?: number;
  type: 'market' | 'limit';
}

export interface Balance {
  balance: number;
  available_balance: number;
  reserved_balance: number;
}

export class KalshiAPI {
  private client: AxiosInstance;
  private token: string | null = null;
  private baseURL = 'https://trading-api.kalshi.com/trade-api/v2';
  
  constructor() {
    this.client = axios.create({
      baseURL: this.baseURL,
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: 30000,
    });

    this.client.interceptors.request.use((config) => {
      if (this.token) {
        config.headers.Authorization = `Bearer ${this.token}`;
      }
      return config;
    });
  }

  async login(credentials: KalshiCredentials): Promise<boolean> {
    try {
      const response = await this.client.post('/login', {
        email: credentials.email,
        password: credentials.password,
      });
      
      this.token = response.data.token;
      return true;
    } catch (error) {
      console.error('Login failed:', error);
      return false;
    }
  }

  async loginWithApiKey(apiKey: string): Promise<boolean> {
    try {
      // Kalshi API keys are used directly as bearer tokens
      // Set the token first
      this.token = apiKey.trim();
      
      // Verify the token works by making a test request to a simple endpoint
      try {
        const response = await this.client.get('/exchange/status');
        if (response.status === 200) {
          return true;
        }
      } catch (testError) {
        console.error('Exchange status check failed, trying balance:', testError);
      }
      
      // If that fails, try the balance endpoint
      const response = await this.client.get('/portfolio/balance');
      return response.status === 200;
    } catch (error: any) {
      console.error('API key authentication failed:', error.response?.data || error.message);
      this.token = null;
      return false;
    }
  }

  async getMarkets(filters?: {
    category?: string;
    status?: string;
    limit?: number;
    cursor?: string;
  }): Promise<Market[]> {
    try {
      const response = await this.client.get('/markets', { params: filters });
      return response.data.markets || [];
    } catch (error) {
      console.error('Failed to fetch markets:', error);
      return [];
    }
  }

  async getMarket(marketId: string): Promise<Market | null> {
    try {
      const response = await this.client.get(`/markets/${marketId}`);
      return response.data.market || null;
    } catch (error) {
      console.error('Failed to fetch market:', error);
      return null;
    }
  }

  async getMarketHistory(marketId: string, limit: number = 100): Promise<any[]> {
    try {
      const response = await this.client.get(`/markets/${marketId}/history`, {
        params: { limit }
      });
      return response.data.history || [];
    } catch (error) {
      console.error('Failed to fetch market history:', error);
      return [];
    }
  }

  async getPositions(): Promise<Position[]> {
    try {
      const response = await this.client.get('/portfolio/positions');
      return response.data.positions || [];
    } catch (error) {
      console.error('Failed to fetch positions:', error);
      return [];
    }
  }

  async getBalance(): Promise<Balance | null> {
    try {
      const response = await this.client.get('/portfolio/balance');
      return response.data.balance || null;
    } catch (error) {
      console.error('Failed to fetch balance:', error);
      return null;
    }
  }

  async placeTrade(order: TradeOrder): Promise<boolean> {
    try {
      await this.client.post('/portfolio/orders', {
        market_id: order.market_id,
        side: order.side,
        action: order.action,
        count: order.quantity,
        ...(order.type === 'limit' && { yes_price: order.price }),
        type: order.type,
      });
      return true;
    } catch (error) {
      console.error('Failed to place trade:', error);
      return false;
    }
  }

  async cancelOrder(orderId: string): Promise<boolean> {
    try {
      await this.client.delete(`/portfolio/orders/${orderId}`);
      return true;
    } catch (error) {
      console.error('Failed to cancel order:', error);
      return false;
    }
  }

  isAuthenticated(): boolean {
    return this.token !== null;
  }

  logout(): void {
    this.token = null;
  }
}

export const kalshiAPI = new KalshiAPI();
