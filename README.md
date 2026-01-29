# Stock Analyzer CLI 📈

A powerful command-line tool for comprehensive stock analysis using real-time market data and technical indicators.

## Features ✨

- **Real-time Stock Data**: Fetches live stock data from Yahoo Finance
- **Technical Analysis**: Multiple technical indicators (RSI, MACD, Moving Averages, Bollinger Bands)
- **Trading Signals**: Generates BUY/SELL signals based on technical analysis
- **Smart Symbol Resolution**: Supports both company names and ticker symbols
- **Multiple Output Formats**: Console table view and JSON output
- **Save Analysis**: Export results to JSON files
- **Indian Market Focus**: Optimized for NSE/BSE stocks

## Quick Start 🚀

### 1. Setup
```bash
# Run the setup script
./setup.sh

# Or manual setup:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
chmod +x stock_analyzer_cli.py
```

### 2. Basic Usage
```bash
# Activate environment
source venv/bin/activate

# Analyze a stock by name
python stock_analyzer_cli.py RELIANCE

# Analyze by ticker
python stock_analyzer_cli.py TCS.NS

# Analyze by company name (use quotes for spaces)
python stock_analyzer_cli.py "HDFC BANK"
```

## Usage Examples 📊

### Basic Analysis
```bash
# Reliance Industries analysis
python stock_analyzer_cli.py RELIANCE

# TCS analysis with verbose output
python stock_analyzer_cli.py TCS -v

# CDSL analysis and save to file
python stock_analyzer_cli.py CDSL --save
```

### Output Formats
```bash
# JSON output (for integration with other tools)
python stock_analyzer_cli.py BSE --json

# Only technical indicators
python stock_analyzer_cli.py INFY --indicators-only

# Verbose mode for debugging
python stock_analyzer_cli.py "TATA STEEL" -v
```

### Advanced Usage
```bash
# Analyze and save with verbose output
python stock_analyzer_cli.py "CHENNAI PETROLEUM" -v --save

# Get help
python stock_analyzer_cli.py --help
```

## Supported Stocks 🏢

The tool supports Indian stocks listed on NSE/BSE. It can resolve:

- **Company Names**: `RELIANCE`, `"HDFC BANK"`, `"TATA STEEL"`
- **Ticker Symbols**: `RELIANCE.NS`, `TCS.BO`, `INFY.NS`
- **Common Abbreviations**: `TCS`, `INFY`, `SBI`, `ITC`

### Pre-configured Mappings
- RELIANCE → RELIANCE.NS
- TCS → TCS.NS
- HDFC/HDFC BANK → HDFCBANK.NS
- ICICI/ICICI BANK → ICICIBANK.NS
- SBI → SBIN.NS
- WIPRO → WIPRO.NS
- AIRTEL → BHARTIARTL.NS
- CDSL → CDSL.NS
- BSE → BSE.NS
- And many more...

## Technical Indicators 📊

### Moving Averages
- **SMA 5, 10, 20**: Simple Moving Averages
- **EMA 12, 26**: Exponential Moving Averages

### Momentum Indicators
- **RSI (14)**: Relative Strength Index
- **MACD**: Moving Average Convergence Divergence

### Volatility Indicators
- **Bollinger Bands**: Price volatility bands
- **Volume Analysis**: Volume vs. average comparison

## Trading Signals 🎯

The tool generates various trading signals:

### BUY Signals
- **SMA Golden Cross**: Price > SMA5 > SMA20
- **RSI Oversold**: RSI < 30
- **MACD Bullish**: MACD above signal line
- **Bollinger Bounce**: Price at lower band
- **High Volume Breakout**: Strong volume with price increase
- **Day High Breakout**: Breaking daily resistance

### SELL Signals
- **SMA Death Cross**: Price < SMA5 < SMA20
- **RSI Overbought**: RSI > 70
- **MACD Bearish**: MACD below signal line
- **Bollinger Resistance**: Price at upper band
- **High Volume Breakdown**: Strong volume with price decrease
- **Day Low Breakdown**: Breaking daily support

## Sample Output 📋

```
🔍 Stock Analyzer CLI - 2024-11-08 19:30:15
Analyzing: RELIANCE

📊 Reliance Industries Limited (RELIANCE.NS)
================================================================================
💰 Current Price: ₹2,456.75
📊 Previous Close: ₹2,443.20
📈 Change: +₹13.55 (+0.55%)
📈 Day Range: ₹2,438.10 - ₹2,467.80
📦 Volume: 4,523,670
🏆 Market Cap: ₹16.6L Cr
📈 P/E Ratio: 26.45
📊 52W Range: ₹2,220.30 - ₹3,024.90
🏭 Sector: Energy
================================================================================

🔍 TECHNICAL INDICATORS
--------------------------------------------------
📈 Moving Averages:
   SMA_5: ₹2,451.20
   SMA_10: ₹2,445.60
   SMA_20: ₹2,438.90
📊 RSI(14): 58.2 (Neutral)
📊 MACD: 12.45 (Signal: 8.32) - Bullish
📊 Bollinger Bands: ₹2,401.50 | ₹2,438.90 | ₹2,476.30

📈 TRADING SIGNALS (2 total)
================================================================================

🟢 BUY SIGNALS (2):
------------------------------------------------------------
1. SMA Golden Cross (Confidence: High)
   💰 Entry Price: ₹2,456.75
   💡 Reason: Price (₹2456.75) > SMA5 (₹2451.20) > SMA20 (₹2438.90)

2. MACD Bullish (Confidence: Medium)
   💰 Entry Price: ₹2,456.75
   💡 Reason: MACD above signal line and positive

================================================================================
💡 IMPORTANT DISCLAIMER:
- This analysis uses real market data and technical indicators
- Signals are for educational/research purposes only
- Always do your own research and risk assessment
- Use proper position sizing and risk management
- This is NOT financial advice
================================================================================

💾 Analysis saved to: RELIANCE_analysis_20241108_1930.json
```

## Command Line Options 🛠️

```
usage: stock_analyzer_cli.py [-h] [-v] [--json] [--save] [--indicators-only] stock

Stock Analyzer CLI - Comprehensive stock analysis tool

positional arguments:
  stock              Stock ticker symbol or company name (e.g., RELIANCE, TCS, "HDFC BANK")

optional arguments:
  -h, --help         show this help message and exit
  -v, --verbose      Enable verbose output
  --json             Output results in JSON format
  --save             Save analysis results to file
  --indicators-only  Show only technical indicators
```

## Requirements 📦

- Python 3.8+
- yfinance >= 0.2.0
- pandas >= 1.3.0
- numpy >= 1.21.0

See `requirements.txt` for complete dependencies.

## File Structure 📁

```
algo/
├── stock_analyzer_cli.py      # Main CLI tool
├── setup.sh                   # Setup script
├── requirements.txt           # Dependencies
├── README.md                 # This file
├── cdsl_analysis.py          # Legacy CDSL analyzer
├── real_bse_analysis.py      # Legacy BSE analyzer
└── venv/                     # Virtual environment (after setup)
```

## Troubleshooting 🔧

### Common Issues

1. **ModuleNotFoundError**: Make sure virtual environment is activated
   ```bash
   source venv/bin/activate
   ```

2. **No data found**: Check if stock symbol is correct
   ```bash
   # Try different variations
   python stock_analyzer_cli.py RELIANCE.NS
   python stock_analyzer_cli.py RELIANCE.BO
   ```

3. **Network issues**: The tool fetches real-time data from Yahoo Finance
   - Check internet connection
   - Yahoo Finance may have temporary restrictions

### Getting Help

```bash
# Show help
python stock_analyzer_cli.py --help

# Test with a known stock
python stock_analyzer_cli.py TCS -v

# Check dependencies
pip list | grep yfinance
```

## Contributing 🤝

Feel free to:
- Report bugs
- Suggest new features
- Add support for more markets
- Improve technical indicators

## Disclaimer ⚠️

This tool is for educational and research purposes only. The analysis and signals generated should not be considered as financial advice. Always:

- Do your own research
- Consult with financial advisors
- Use proper risk management
- Never invest more than you can afford to lose

## RSI Crossover Strategy 🎯

### New Addition: Advanced RSI Strategy with Volume Analysis

A specialized script that identifies RSI crossovers above 40 with high potential to reach RSI 70, using volume analysis and multiple technical indicators.

#### Features:
- **RSI Crossover Detection**: Identifies when RSI crosses above 40
- **6-Factor Scoring System**: Evaluates RSI 70 potential
- **Volume Analysis**: Volume spikes, OBV, volume ratios
- **Multi-Timeframe Support**: Works with any timeframe data
- **Backtesting Capability**: Built-in strategy performance testing

#### Quick Usage:
```bash
# Test with sample data
python test_rsi_strategy.py

# Use with real data
python -c "
import yfinance as yf
from test_rsi_strategy import RSICrossoverStrategy
data = yf.download('RELIANCE.NS', start='2023-01-01')
data.columns = data.columns.droplevel(1)
data = data.rename(columns=str.lower)
strategy = RSICrossoverStrategy()
analyzed = strategy.analyze_data(data)
alerts = strategy.generate_alerts(analyzed)
print(f'Found {len(alerts)} RSI crossover signals')
"
```

#### Files:
- `rsi_crossover_strategy.py`: Complete strategy with visualization
- `test_rsi_strategy.py`: Simplified version for testing
- Both scripts are standalone and can be used independently

## License 📄

This project is open source. Use responsibly and at your own risk.

---

**Happy Trading! 📈🚀**# Stock-Portfolio-Analyzer
