# Kalshi Trading Platform

Advanced prediction market analysis and automated trading platform for Kalshi markets. This application provides sophisticated market analysis, risk management, and automated trading capabilities.

## ⚠️ Important Disclaimer

**This platform is for educational and informational purposes only. Trading involves significant financial risk.**

- **No Guaranteed Profits**: This system cannot guarantee profits or consistent returns
- **Financial Risk**: You can lose all invested capital
- **Market Risk**: Prediction markets are volatile and difficult to predict
- **Use at Your Own Risk**: Always understand the risks before trading
- **Not Financial Advice**: This tool does not provide financial, investment, or trading advice

## 🚀 Features

### Market Intelligence
- **Real-time Market Data**: Live market prices, volume, and liquidity
- **Advanced Analysis**: Statistical modeling and probability calculations
- **Edge Detection**: Identifies mispriced markets with potential value
- **Sentiment Analysis**: Market momentum and crowd behavior insights

### Risk Management
- **Position Sizing**: Kelly Criterion-based position sizing
- **Portfolio Limits**: Maximum exposure and position limits
- **Stop Loss**: Automatic stop-loss calculation and monitoring
- **Risk Scoring**: Real-time portfolio risk assessment

### Automated Trading
- **Market Scanning**: Continuous market opportunity scanning
- **Signal Generation**: Automated trading signals based on analysis
- **Trade Execution**: Automated trade execution with safeguards
- **Manual Approval**: Optional manual approval for all trades

### Analytics
- **Performance Tracking**: Track wins, losses, and returns
- **Portfolio Overview**: Real-time portfolio value and P&L
- **Risk Monitoring**: Live risk metrics and warnings
- **Trade History**: Complete execution history with analytics

## 🛠️ Tech Stack

- **Frontend**: Next.js 15, React, TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **Charts**: Recharts
- **API Integration**: Axios
- **Icons**: Lucide React

## 📦 Installation

### Prerequisites
- Node.js 18+ and npm
- Kalshi account with API access
- API credentials from Kalshi

### Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd kalshi-trading-platform
```

2. **Install dependencies**
```bash
npm install
```

3. **Configure environment**
```bash
cp .env.example .env.local
```

Edit `.env.local` with your credentials:
```env
KALSHI_EMAIL=your_email@example.com
KALSHI_PASSWORD=your_password
```

4. **Run development server**
```bash
npm run dev
```

5. **Open application**
Navigate to [http://localhost:3000](http://localhost:3000)

## 🎯 Usage Guide

### Getting Started

1. **Login**: Enter your Kalshi credentials on the login page
2. **Scan Markets**: Click "Scan Markets" to analyze available opportunities
3. **Review Analysis**: Review market analyses, trading signals, and risk metrics
4. **Configure Trading**: Set your risk parameters and trading preferences
5. **Start Trading**: Enable auto-trading or manually approve trades

### Market Analysis

The platform analyzes markets using multiple factors:

- **Edge Score**: Difference between fair value and market price
- **Confidence Score**: Reliability of the analysis (liquidity, volume, data)
- **Risk Level**: Low, Medium, or High based on volatility and liquidity
- **Recommendation**: Strong Buy, Buy, Hold, Sell, Strong Sell

### Risk Management

Built-in risk controls:

- **Position Limits**: Max 5% per position (configurable)
- **Portfolio Limits**: Max 30% total exposure (configurable)
- **Loss Limits**: Max 2% loss per trade, 10% daily loss
- **Liquidity Filters**: Minimum liquidity requirements
- **Confidence Filters**: Minimum confidence thresholds

### Trading Modes

**Manual Mode** (Recommended for Beginners)
- Review all trading signals
- Manually approve or reject each trade
- Full control over execution

**Auto-Trading Mode** (Advanced Users)
- Automated market scanning
- Automatic trade execution
- Still subject to all risk controls

## 📊 System Architecture

### Core Components

**KalshiAPI** (`lib/kalshi-api.ts`)
- API client for Kalshi integration
- Authentication and session management
- Market data fetching
- Order placement and management

**MarketAnalyzer** (`lib/market-analyzer.ts`)
- Market analysis and valuation
- Statistical modeling
- Edge detection
- Signal generation

**RiskManager** (`lib/risk-manager.ts`)
- Risk assessment and scoring
- Position sizing calculations
- Portfolio risk monitoring
- Trade approval logic

**TradingEngine** (`lib/trading-engine.ts`)
- Market scanning orchestration
- Signal processing
- Trade execution
- Position monitoring

## ⚙️ Configuration

### Risk Parameters

Edit in the dashboard or via environment variables:

```typescript
{
  maxPositionSize: 5,        // Max % per position
  maxTotalExposure: 30,      // Max % total exposure
  maxLossPerTrade: 2,        // Max % loss per trade
  maxDailyLoss: 10,          // Max % daily loss
  minLiquidity: 30,          // Min liquidity score
  minConfidence: 50,         // Min confidence score
  maxConcurrentPositions: 10 // Max open positions
}
```

### Trading Parameters

```typescript
{
  autoTradeEnabled: false,       // Enable auto-trading
  minEdgeThreshold: 8,           // Min edge to trade (%)
  minConfidenceThreshold: 50,    // Min confidence to trade
  scanIntervalSeconds: 60,       // Market scan interval
  requireManualApproval: true    // Require approval
}
```

## 🔒 Security

- **Credentials**: Store credentials securely, never commit to git
- **API Keys**: Use environment variables for sensitive data
- **Local Storage**: Credentials are stored in browser memory only
- **No Sharing**: Never share your credentials or API keys

## 🧪 Testing

Before live trading:

1. **Start with small positions**: Test with minimal capital
2. **Monitor closely**: Watch the first few trades carefully
3. **Verify analysis**: Cross-check signals with your own research
4. **Test risk controls**: Ensure stop-losses and limits work correctly

## 📈 Performance Tips

1. **Higher Confidence**: Only trade signals with confidence > 70%
2. **Lower Risk**: Start with High Edge + Low Risk markets
3. **Diversify**: Don't concentrate in single category
4. **Monitor**: Regularly check portfolio risk metrics
5. **Adjust**: Fine-tune risk parameters based on results

## 🐛 Troubleshooting

### API Connection Issues
- Verify credentials are correct
- Check Kalshi API status
- Ensure network connectivity

### No Markets Loading
- Click "Scan Markets" to refresh
- Check if markets are currently open
- Verify API authentication

### Trades Not Executing
- Check risk limits aren't exceeded
- Verify sufficient balance
- Ensure liquidity is adequate

## 📝 Development

### Project Structure
```
kalshi-trading-platform/
├── app/                    # Next.js app directory
│   ├── page.tsx           # Main page component
│   ├── layout.tsx         # Root layout
│   └── globals.css        # Global styles
├── components/            # React components
│   ├── Dashboard.tsx      # Main dashboard
│   ├── LoginForm.tsx      # Authentication
│   ├── MarketList.tsx     # Market listings
│   ├── PortfolioOverview.tsx
│   ├── TradingSignals.tsx
│   ├── RiskMonitor.tsx
│   └── PerformanceChart.tsx
├── lib/                   # Core logic
│   ├── kalshi-api.ts      # API client
│   ├── market-analyzer.ts # Analysis engine
│   ├── risk-manager.ts    # Risk management
│   ├── trading-engine.ts  # Trading logic
│   └── store.ts           # State management
└── package.json
```

### Building for Production

```bash
npm run build
npm run start
```

## 🤝 Contributing

This is a personal project. Feel free to fork and adapt for your needs.

## 📄 License

MIT License - See LICENSE file for details

## ⚡ Roadmap

Future enhancements:
- [ ] Machine learning models for prediction
- [ ] Backtesting framework
- [ ] Multi-account support
- [ ] Advanced charting
- [ ] Mobile app
- [ ] Telegram notifications
- [ ] Strategy builder
- [ ] Paper trading mode

## 📞 Support

For Kalshi API issues, contact Kalshi support.
For platform bugs, open an issue in the repository.

## ⚠️ Final Warning

**NEVER risk money you cannot afford to lose. This platform is a tool, not a guaranteed profit system. Always do your own research and understand the risks before trading.**

---

Built with ❤️ for prediction market traders
