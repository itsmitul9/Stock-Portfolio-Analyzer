#!/usr/bin/env python3
"""
CSV-Based RSI Screener
Reads stock symbols from CSV file and screens for RSI oversold conditions

Usage:
python csv_based_rsi_screener.py [CSV_FILE] [RSI_THRESHOLD]

CSV File Format:
- Must have a column named 'Symbol' or 'SYMBOL' or 'symbol'
- Each symbol should have .NS suffix for Indian stocks
- Example: RELIANCE.NS, TCS.NS, etc.

Default: Uses nifty500.csv if available, otherwise creates sample CSV
"""

import sys
import os
import pandas as pd
import yfinance as yf
import talib
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def load_symbols_from_csv(csv_file):
    """Load stock symbols from CSV file"""
    try:
        df = pd.read_csv(csv_file)

        # Find symbol column (case insensitive)
        symbol_col = None
        for col in df.columns:
            if col.lower() in ['symbol', 'symbols', 'ticker', 'stock']:
                symbol_col = col
                break

        if symbol_col is None:
            print("❌ Error: CSV must have a column named 'Symbol', 'symbol', 'ticker', or 'stock'")
            return []

        symbols = df[symbol_col].tolist()

        # Clean symbols and add .NS if not present
        clean_symbols = []
        for symbol in symbols:
            if pd.isna(symbol):
                continue
            symbol = str(symbol).strip()
            if symbol and not symbol.endswith('.NS'):
                symbol += '.NS'
            if symbol:
                clean_symbols.append(symbol)

        print(f"✅ Loaded {len(clean_symbols)} symbols from {csv_file}")
        return clean_symbols

    except FileNotFoundError:
        print(f"❌ Error: File '{csv_file}' not found")
        return []
    except Exception as e:
        print(f"❌ Error reading CSV: {str(e)}")
        return []

def create_sample_csv_files():
    """Create sample CSV files for different indices"""

    # Nifty 50 symbols
    nifty50_symbols = [
        "RELIANCE", "TCS", "HDFCBANK", "INFY", "ICICIBANK",
        "HINDUNILVR", "ITC", "SBIN", "BHARTIARTL", "KOTAKBANK",
        "LT", "ASIANPAINT", "AXISBANK", "MARUTI", "SUNPHARMA",
        "TITAN", "ULTRACEMCO", "WIPRO", "NESTLEIND", "POWERGRID",
        "HCLTECH", "BAJFINANCE", "BAJAJFINSV", "TATASTEEL", "M&M",
        "TECHM", "COALINDIA", "NTPC", "ADANIPORTS", "JSWSTEEL",
        "GRASIM", "HINDALCO", "INDUSINDBK", "HEROMOTOCO", "CIPLA",
        "EICHERMOT", "BRITANNIA", "DRREDDY", "APOLLOHOSP", "DIVISLAB",
        "TATACONSUM", "GODREJCP", "PIDILITIND", "DABUR", "MARICO",
        "VOLTAS", "HAVELLS", "BERGEPAINT", "PAGEIND", "COLPAL"
    ]

    # Create Nifty 50 CSV
    nifty50_df = pd.DataFrame({'Symbol': nifty50_symbols})
    nifty50_df.to_csv('nifty50.csv', index=False)
    print("📄 Created nifty50.csv with 50 stocks")

    # Sample Nifty 500 (top 100 stocks for demo)
    nifty500_sample = nifty50_symbols + [
        "ADANIENT", "ADANIGREEN", "ADANIPOWER", "AIAENG", "AJANTPHARM",
        "ALKEM", "AMBUJACEM", "AUROPHARMA", "BALKRISIND", "BANDHANBNK",
        "BANKBARODA", "BATAINDIA", "BEL", "BHEL", "BIOCON",
        "BOSCHLTD", "BPCL", "CADILAHC", "CANBK", "CHAMBLFERT",
        "CHOLAFIN", "COLPAL", "CONCOR", "COROMANDEL", "CUMMINSIND",
        "DABUR", "DEEPAKNTR", "DIVI", "DLF", "FEDERALBNK",
        "GAIL", "GLENMARK", "GMRINFRA", "GODREJCP", "GRANULES",
        "GUJGASLTD", "HAL", "HAVELLS", "HDFCAMC", "HDFCLIFE",
        "HINDCOPPER", "HINDPETRO", "HINDUNILVR", "HINDZINC", "IBULHSGFIN",
        "IDEA", "IDFCFIRSTB", "IEX", "IGL", "INDIGO"
    ]

    nifty500_df = pd.DataFrame({'Symbol': nifty500_sample})
    nifty500_df.to_csv('nifty500_sample.csv', index=False)
    print("📄 Created nifty500_sample.csv with 100 stocks")

    return 'nifty50.csv'

def calculate_rsi_with_details(symbol, data, rsi_period=14):
    """Calculate RSI and return detailed information"""
    try:
        # Calculate RSI
        rsi = talib.RSI(data['Close'].values, timeperiod=rsi_period)

        current_rsi = rsi[-1]
        current_price = data['Close'].iloc[-1]
        current_date = data.index[-1]

        # Calculate additional metrics
        previous_rsi = rsi[-2] if len(rsi) > 1 else current_rsi
        rsi_trend = "↗" if current_rsi > previous_rsi else "↘" if current_rsi < previous_rsi else "→"

        # Volume analysis
        volume_20d_avg = data['Volume'].rolling(window=20).mean().iloc[-1]
        current_volume = data['Volume'].iloc[-1]
        volume_ratio = current_volume / volume_20d_avg if volume_20d_avg > 0 else 1

        return {
            'symbol': symbol,
            'price': round(current_price, 2),
            'rsi': round(current_rsi, 2),
            'rsi_trend': rsi_trend,
            'volume_ratio': round(volume_ratio, 2),
            'date': current_date.strftime('%Y-%m-%d')
        }

    except Exception as e:
        return None

def screen_csv_stocks(csv_file, rsi_threshold=30, period="3mo"):
    """Screen stocks from CSV file for RSI oversold conditions"""

    # Load symbols
    symbols = load_symbols_from_csv(csv_file)
    if not symbols:
        return []

    print(f"\n🔍 Screening {len(symbols)} stocks for RSI <= {rsi_threshold}")
    print(f"📅 Using {period} data period")
    print("=" * 80)

    oversold_stocks = []
    processed = 0

    for i, symbol in enumerate(symbols, 1):
        try:
            print(f"  {i:3d}/{len(symbols)}: {symbol:<20}", end="")

            # Fetch data
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period, interval="1d")

            if data.empty:
                print(" - No data")
                continue

            # Calculate RSI
            rsi_data = calculate_rsi_with_details(symbol, data)

            if rsi_data is None:
                print(" - RSI calculation failed")
                continue

            current_rsi = rsi_data['rsi']
            processed += 1

            if current_rsi <= rsi_threshold:
                oversold_stocks.append(rsi_data)
                print(f" - ✅ RSI: {current_rsi:5.1f} {rsi_data['rsi_trend']}")
            else:
                print(f" - RSI: {current_rsi:5.1f} {rsi_data['rsi_trend']}")

        except Exception as e:
            print(f" - Error: {str(e)}")
            continue

    print(f"\n📊 Processed: {processed}/{len(symbols)} stocks successfully")
    return oversold_stocks

def display_results(oversold_stocks, rsi_threshold, csv_file):
    """Display formatted results"""

    print("\n" + "=" * 80)
    print(f"📈 RSI OVERSOLD SCREENING RESULTS")
    print(f"📁 Source: {csv_file}")
    print(f"🎯 RSI Threshold: ≤ {rsi_threshold}")
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    if not oversold_stocks:
        print(f"📭 No stocks found with RSI ≤ {rsi_threshold}")
        return

    # Sort by RSI (most oversold first)
    oversold_stocks.sort(key=lambda x: x['rsi'])

    print(f"\n🔴 OVERSOLD STOCKS FOUND: {len(oversold_stocks)}")
    print("-" * 70)
    print(f"{'SYMBOL':<20} {'PRICE':<12} {'RSI':<8} {'TREND':<8} {'VOLUME':<8}")
    print("-" * 70)

    for stock in oversold_stocks:
        vol_indicator = "High" if stock['volume_ratio'] > 1.5 else "Low" if stock['volume_ratio'] < 0.8 else "Norm"

        print(f"{stock['symbol']:<20} "
              f"₹{stock['price']:<11} "
              f"{stock['rsi']:<7.1f} "
              f"{stock['rsi_trend']:<8} "
              f"{vol_indicator:<8}")

    # Summary statistics
    print("-" * 70)
    print(f"📊 SUMMARY:")
    print(f"• Total oversold stocks: {len(oversold_stocks)}")
    print(f"• Lowest RSI: {min(s['rsi'] for s in oversold_stocks):.1f}")
    print(f"• Average RSI: {sum(s['rsi'] for s in oversold_stocks) / len(oversold_stocks):.1f}")

    # Categorize by severity
    extremely_oversold = [s for s in oversold_stocks if s['rsi'] <= 20]
    very_oversold = [s for s in oversold_stocks if 20 < s['rsi'] <= 25]
    moderately_oversold = [s for s in oversold_stocks if 25 < s['rsi'] <= 30]

    if extremely_oversold:
        print(f"• Extremely oversold (≤20): {len(extremely_oversold)}")
    if very_oversold:
        print(f"• Very oversold (20-25): {len(very_oversold)}")
    if moderately_oversold:
        print(f"• Moderately oversold (25-30): {len(moderately_oversold)}")

def save_results(oversold_stocks, csv_file, rsi_threshold):
    """Save results to CSV"""
    if not oversold_stocks:
        return

    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    output_file = f"rsi_oversold_results_{timestamp}.csv"

    df = pd.DataFrame(oversold_stocks)
    df['source_file'] = csv_file
    df['rsi_threshold'] = rsi_threshold
    df['scan_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    df.to_csv(output_file, index=False)
    print(f"💾 Results saved to: {output_file}")

def main():
    """Main function"""

    # Parse command line arguments
    csv_file = "nifty50.csv"  # default
    rsi_threshold = 30  # default

    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    if len(sys.argv) > 2:
        try:
            rsi_threshold = float(sys.argv[2])
        except ValueError:
            print("Invalid RSI threshold. Using default value of 30.")

    # Check if CSV file exists, create sample if not
    if not os.path.exists(csv_file):
        print(f"📁 CSV file '{csv_file}' not found.")
        print("🔧 Creating sample CSV files...")
        csv_file = create_sample_csv_files()

    # Run screening
    oversold_stocks = screen_csv_stocks(csv_file, rsi_threshold)

    # Display and save results
    display_results(oversold_stocks, rsi_threshold, csv_file)
    save_results(oversold_stocks, csv_file, rsi_threshold)

    print("\n" + "=" * 80)
    print("💡 USAGE EXAMPLES:")
    print("• python csv_based_rsi_screener.py nifty50.csv 30")
    print("• python csv_based_rsi_screener.py nifty500.csv 25")
    print("• python csv_based_rsi_screener.py my_stocks.csv 35")
    print("\n⚠️  DISCLAIMER: Educational use only. Do your own research!")
    print("=" * 80)

if __name__ == "__main__":
    main()