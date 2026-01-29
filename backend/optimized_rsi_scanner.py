#!/usr/bin/env python3
"""
Optimized RSI Scanner - Focus on RSI 40-50 with High Volume & Momentum
======================================================================

Refined criteria for finding realistic trading opportunities
"""

import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import warnings
import time
import os
warnings.filterwarnings('ignore')

def calculate_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
    """Calculate RSI"""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def analyze_single_stock(symbol: str, data: pd.DataFrame) -> dict:
    """Analyze single stock for entry opportunity"""

    # Clean data
    data.columns = [col.lower() for col in data.columns]

    # Calculate RSI
    data['rsi'] = calculate_rsi(data['close'])

    # Volume analysis
    data['volume_ma'] = data['volume'].rolling(window=20).mean()
    data['volume_ratio'] = data['volume'] / data['volume_ma']

    # Price momentum
    data['price_change_5d'] = ((data['close'] - data['close'].shift(5)) / data['close'].shift(5)) * 100
    data['price_change_10d'] = ((data['close'] - data['close'].shift(10)) / data['close'].shift(10)) * 100

    # MACD
    ema12 = data['close'].ewm(span=12).mean()
    ema26 = data['close'].ewm(span=26).mean()
    data['macd'] = ema12 - ema26
    data['macd_signal'] = data['macd'].ewm(span=9).mean()

    # Moving averages
    data['sma_10'] = data['close'].rolling(window=10).mean()
    data['sma_20'] = data['close'].rolling(window=20).mean()
    data['sma_50'] = data['close'].rolling(window=50).mean()
    data['sma_220'] = data['close'].rolling(window=220).mean()

    # Get latest values
    latest = data.iloc[-1]

    # Check basic criteria
    rsi = latest['rsi']
    volume_ratio = latest['volume_ratio']
    price_change_5d = latest['price_change_5d']

    # Relaxed criteria for realistic opportunities
    rsi_in_range = 40 <= rsi <= 55  # Slightly broader range
    volume_good = volume_ratio > 1.1  # Above average volume

    # DMA filters - stock should be above both 50 DMA and 220 DMA
    above_50dma = latest['close'] > latest['sma_50'] if not pd.isna(latest['sma_50']) else False
    above_220dma = latest['close'] > latest['sma_220'] if not pd.isna(latest['sma_220']) else False
    dma_criteria = above_50dma and above_220dma

    momentum_positive = (
        price_change_5d > -2 or  # Not falling too fast
        latest['macd'] > latest['macd_signal'] or  # MACD bullish
        latest['close'] > latest['sma_10']  # Above short MA
    )

    # Calculate momentum score
    momentum_score = 0
    if volume_ratio > 1.3: momentum_score += 1  # Strong volume
    if price_change_5d > 1: momentum_score += 1  # Price rising
    if latest['macd'] > latest['macd_signal']: momentum_score += 1  # MACD bullish
    if latest['close'] > latest['sma_10']: momentum_score += 1  # Above short MA
    if latest['close'] > latest['sma_20']: momentum_score += 1  # Above medium MA
    if above_50dma: momentum_score += 1  # Above 50 DMA
    if above_220dma: momentum_score += 1  # Above 220 DMA
    if latest['price_change_10d'] > 0: momentum_score += 1  # 10-day positive

    # RSI trend (is it rising?)
    rsi_values = data['rsi'].tail(5).dropna()
    if len(rsi_values) >= 3:
        rsi_trend = rsi_values.iloc[-1] - rsi_values.iloc[-3]  # 3-day RSI change
    else:
        rsi_trend = 0

    if rsi_in_range and volume_good and momentum_positive and dma_criteria:
        return {
            'symbol': symbol,
            'current_rsi': rsi,
            'rsi_trend': rsi_trend,
            'current_price': latest['close'],
            'volume_ratio': volume_ratio,
            'momentum_score': momentum_score,
            'price_change_5d': price_change_5d,
            'price_change_10d': latest['price_change_10d'],
            'macd_bullish': latest['macd'] > latest['macd_signal'],
            'above_sma10': latest['close'] > latest['sma_10'],
            'above_sma20': latest['close'] > latest['sma_20'],
            'above_sma50': above_50dma,
            'above_sma220': above_220dma,
        }

    return None

def scan_csv_file(csv_file: str, max_results: int = 15) -> pd.DataFrame:
    """Scan CSV file for opportunities"""
    print(f"\nScanning {csv_file}...")
    print("-" * 40)

    try:
        df = pd.read_csv(csv_file)
        symbols = df['Symbol'].tolist()

        results = []
        analyzed = 0

        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)  # Increased to 1 year for 220 DMA calculation

        for symbol in symbols:
            if len(results) >= max_results:
                break

            symbol_ns = f"{symbol}.NS"

            try:
                ticker = yf.Ticker(symbol_ns)
                data = ticker.history(start=start_date.strftime('%Y-%m-%d'))

                if data.empty or len(data) < 250:  # Need at least 250 days for 220 DMA
                    continue

                analyzed += 1

                analysis = analyze_single_stock(symbol, data)

                if analysis:
                    # Get company info
                    try:
                        info = ticker.info
                        analysis['company_name'] = info.get('longName', symbol)[:30]
                        analysis['sector'] = info.get('sector', 'Unknown')[:15]
                    except:
                        analysis['company_name'] = symbol
                        analysis['sector'] = 'Unknown'

                    results.append(analysis)
                    print(f"✅ {symbol:12} RSI:{analysis['current_rsi']:5.1f} Vol:{analysis['volume_ratio']:4.1f}x Score:{analysis['momentum_score']}/8")

                time.sleep(0.05)  # Rate limiting

            except Exception as e:
                continue

        print(f"Found {len(results)} opportunities from {analyzed} stocks")

        if results:
            return pd.DataFrame(results).sort_values(['momentum_score', 'current_rsi'], ascending=[False, True])
        else:
            return pd.DataFrame()

    except Exception as e:
        print(f"Error processing {csv_file}: {e}")
        return pd.DataFrame()

def display_results(results_df: pd.DataFrame, title: str):
    """Display formatted results"""
    if results_df.empty:
        return

    print(f"\n{'='*80}")
    print(f"{title}")
    print("="*80)
    print(f"{'Symbol':<12} {'Company':<25} {'RSI':<6} {'Trend':<6} {'Vol':<6} {'Score':<6} {'5d%':<6} {'DMA':<6}")
    print("-"*86)

    for _, row in results_df.iterrows():
        trend_symbol = "↑" if row['rsi_trend'] > 0.5 else "↓" if row['rsi_trend'] < -0.5 else "→"
        dma_status = "50+220" if row['above_sma50'] and row['above_sma220'] else "FAIL"

        print(f"{row['symbol']:<12} {row['company_name']:<25} {row['current_rsi']:5.1f} "
              f"{trend_symbol:<6} {row['volume_ratio']:5.1f} {row['momentum_score']:5d}/8 "
              f"{row['price_change_5d']:5.1f} {dma_status:<6}")

def generate_trading_recommendations(results_df: pd.DataFrame):
    """Generate specific trading recommendations"""
    if results_df.empty:
        return

    print(f"\n{'='*60}")
    print("TRADING RECOMMENDATIONS")
    print("="*60)

    # Filter for high-quality opportunities
    high_quality = results_df[
        (results_df['momentum_score'] >= 5) &
        (results_df['volume_ratio'] > 1.2)
    ]

    if high_quality.empty:
        print("No high-quality opportunities found with current criteria")
        return

    print("HIGH QUALITY OPPORTUNITIES (Score ≥5, Volume >1.2x):")
    print("-" * 60)

    for i, (_, row) in enumerate(high_quality.head(5).iterrows(), 1):
        recommendation = "STRONG BUY" if row['momentum_score'] >= 6 else "BUY"

        print(f"{i}. {row['symbol']} - {recommendation}")
        print(f"   RSI: {row['current_rsi']:.1f} (Target: 70)")
        print(f"   Volume: {row['volume_ratio']:.1f}x average")
        print(f"   5-day return: {row['price_change_5d']:.1f}%")
        print(f"   Momentum score: {row['momentum_score']}/8")
        print(f"   Above 50/220 DMA: {row['above_sma50']}/{row['above_sma220']}")
        print()

def main():
    """Main function"""
    print("Optimized RSI Scanner - Finding Real Opportunities")
    print("="*60)
    print("Criteria: RSI 40-55, Volume >1.1x avg, Positive momentum")
    print("NEW: Stock must be above both 50 DMA and 220 DMA")
    print()

    csv_files = [
        ('nifty500.csv', 'NIFTY 500'),
        ('nifty500_banking.csv', 'BANKING SECTOR'),
        ('nifty500_technology.csv', 'TECHNOLOGY SECTOR'),
        ('nifty500_fmcg.csv', 'FMCG SECTOR'),
        ('nifty500_pharmaceuticals.csv', 'PHARMA SECTOR'),
    ]

    all_results = []

    for csv_file, title in csv_files:
        if os.path.exists(csv_file):
            results_df = scan_csv_file(csv_file, max_results=10)

            if not results_df.empty:
                display_results(results_df, f"{title} OPPORTUNITIES")
                all_results.append(results_df)

                # Save sector results
                timestamp = datetime.now().strftime('%Y%m%d_%H%M')
                sector_name = csv_file.replace('nifty500_', '').replace('.csv', '').replace('nifty500', 'all')
                output_file = f"rsi_opportunities_{sector_name}_{timestamp}.csv"
                results_df.to_csv(output_file, index=False)
                print(f"Saved to: {output_file}")

    # Combined analysis
    if all_results:
        combined_df = pd.concat(all_results, ignore_index=True)
        combined_sorted = combined_df.sort_values(['momentum_score', 'volume_ratio'], ascending=[False, False])

        print(f"\n{'='*80}")
        print("TOP 10 OVERALL OPPORTUNITIES")
        print("="*80)

        top_10 = combined_sorted.head(10)
        for i, (_, row) in enumerate(top_10.iterrows(), 1):
            print(f"{i:2d}. {row['symbol']:<12} RSI:{row['current_rsi']:5.1f} "
                  f"Vol:{row['volume_ratio']:4.1f}x Score:{row['momentum_score']}/8 "
                  f"Sector:{row['sector']}")

        # Generate recommendations
        generate_trading_recommendations(combined_sorted)

        # Save combined results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        combined_output = f"rsi_opportunities_combined_{timestamp}.csv"
        combined_sorted.to_csv(combined_output, index=False)
        print(f"\nAll results saved to: {combined_output}")
    else:
        print("No opportunities found across all sectors")

if __name__ == "__main__":
    main()