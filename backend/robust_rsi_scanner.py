#!/usr/bin/env python3
"""
Robust RSI Scanner - Handles Delisted/Invalid Stocks
====================================================

This script filters out delisted stocks and handles data issues properly
"""

import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import warnings
import time
import os
import sys
from io import StringIO
warnings.filterwarnings('ignore')

class RobustRSIScanner:
    """RSI Scanner with robust error handling"""

    def __init__(self):
        # Known problematic/delisted stocks to skip
        self.blacklist = {
            'CADILAHC', 'GMRINFRA', 'IBULHSGFIN', 'MCDOWELL-N', 'MINDTREE',
            'SRTRANSFIN', 'ADANIGAS', 'ADANITRANS', 'AVANTI', 'BHARAT22',
            'HEXAWARE', 'INOXLEISUR', 'ISEC', 'JUBILANT', 'L&TFH', 'LAXMIMACH',
            'MAGMA', 'MAHINDCIE', 'MCDOWELL', 'MINDAIND', 'MOTHERSUMI',
            'ORIENT', 'ORIENTREF', 'PIRAMALENT', 'RNAM', 'SFBBANK', 'SPICEJET',
            'STRTECH', 'SWANENERGY', 'SYNDIBANK', 'TATASTLLP', 'UJJIVAN',
            'USTFVCL', 'WABCOINDIA', 'WELSPUNIND', 'PAGEIND', 'BOSCHLTD',
            'MRF', 'SHREECEM', 'APCOTEXIND', 'ATUL', 'FINEORG', 'GILLETTE',
            'HONAUT', 'JETAIRWAYS', 'LINDEINDIA', 'LUXIND', 'NILKAMAL',
            'PFIZER', 'RATNAMANI', 'SANOFI', 'TEAMLEASE'
        }

    def calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """Calculate RSI with error handling"""
        try:
            delta = prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

            # Avoid division by zero
            rs = gain / loss.replace(0, np.nan)
            rsi = 100 - (100 / (1 + rs))
            return rsi
        except Exception:
            return pd.Series([np.nan] * len(prices), index=prices.index)

    def is_stock_valid(self, symbol: str, data: pd.DataFrame) -> bool:
        """Check if stock data is valid for analysis"""
        try:
            if symbol in self.blacklist:
                return False

            if data is None or data.empty:
                return False

            if len(data) < 30:  # Need at least 30 days
                return False

            # Check for sufficient volume
            avg_volume = data['volume'].mean()
            if avg_volume < 10000:  # Very low volume threshold
                return False

            # Check for recent trading activity
            recent_volume = data['volume'].tail(5).mean()
            if recent_volume < 1000:  # Almost no recent activity
                return False

            # Check for reasonable price range
            current_price = data['close'].iloc[-1]
            if current_price < 1 or current_price > 50000:  # Unrealistic prices
                return False

            return True

        except Exception:
            return False

    def fetch_stock_data(self, symbol: str) -> tuple:
        """Fetch stock data with robust error handling"""
        try:
            # Skip blacklisted stocks immediately
            if symbol in self.blacklist:
                return None, f"Blacklisted stock"

            symbol_ns = f"{symbol}.NS"

            # Redirect stderr to capture yfinance warnings
            old_stderr = sys.stderr
            sys.stderr = StringIO()

            ticker = yf.Ticker(symbol_ns)

            end_date = datetime.now()
            start_date = end_date - timedelta(days=90)

            # Try to fetch data
            data = ticker.history(
                start=start_date.strftime('%Y-%m-%d'),
                end=end_date.strftime('%Y-%m-%d'),
                interval='1d',
                timeout=10  # Add timeout
            )

            # Restore stderr
            sys.stderr = old_stderr

            if data is None or data.empty:
                return None, "No data returned"

            # Clean column names
            data.columns = [col.lower() for col in data.columns]

            # Validate the data
            if not self.is_stock_valid(symbol, data):
                return None, "Invalid data quality"

            return data, "Success"

        except Exception as e:
            sys.stderr = old_stderr
            error_msg = str(e)
            if "delisted" in error_msg.lower() or "timezone" in error_msg.lower():
                return None, "Delisted/Timezone issue"
            return None, f"Error: {error_msg[:30]}"

    def analyze_stock_for_rsi_opportunity(self, symbol: str, data: pd.DataFrame) -> dict:
        """Analyze stock for RSI opportunity"""
        try:
            # Calculate RSI
            data['rsi'] = self.calculate_rsi(data['close'])

            # Skip if RSI calculation failed
            if data['rsi'].isna().all():
                return None

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

            # Get latest values
            latest = data.iloc[-1]

            # Skip if critical values are NaN
            if pd.isna(latest['rsi']) or pd.isna(latest['volume_ratio']):
                return None

            rsi = latest['rsi']
            volume_ratio = latest['volume_ratio']
            price_change_5d = latest['price_change_5d']

            # Apply RSI filter (40-55 range)
            if not (40 <= rsi <= 55):
                return None

            # Volume filter
            if volume_ratio < 1.1:
                return None

            # Basic momentum filter
            momentum_positive = (
                price_change_5d > -3 or  # Not falling too fast
                latest['macd'] > latest['macd_signal'] or  # MACD bullish
                latest['close'] > latest['sma_10']  # Above short MA
            )

            if not momentum_positive:
                return None

            # Calculate momentum score
            momentum_score = 0
            if volume_ratio > 1.3: momentum_score += 1
            if price_change_5d > 1: momentum_score += 1
            if latest['macd'] > latest['macd_signal']: momentum_score += 1
            if latest['close'] > latest['sma_10']: momentum_score += 1
            if latest['close'] > latest['sma_20']: momentum_score += 1
            if latest['price_change_10d'] > 0: momentum_score += 1

            # RSI trend
            rsi_values = data['rsi'].tail(5).dropna()
            rsi_trend = rsi_values.iloc[-1] - rsi_values.iloc[0] if len(rsi_values) >= 5 else 0

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
            }

        except Exception as e:
            return None

    def clean_csv_symbols(self, csv_file: str) -> list:
        """Clean and filter CSV symbols"""
        try:
            df = pd.read_csv(csv_file)
            symbols = df['Symbol'].tolist()

            # Remove blacklisted symbols
            clean_symbols = [s for s in symbols if s not in self.blacklist]

            print(f"Original symbols: {len(symbols)}")
            print(f"After filtering: {len(clean_symbols)} ({len(symbols) - len(clean_symbols)} removed)")

            return clean_symbols
        except Exception as e:
            print(f"Error reading {csv_file}: {e}")
            return []

    def scan_csv_for_opportunities(self, csv_file: str, max_results: int = 15) -> pd.DataFrame:
        """Scan CSV with robust error handling"""
        print(f"\n{'='*60}")
        print(f"Scanning {csv_file}")
        print("="*60)

        symbols = self.clean_csv_symbols(csv_file)
        if not symbols:
            return pd.DataFrame()

        results = []
        analyzed = 0
        errors = {'delisted': 0, 'no_data': 0, 'invalid': 0, 'other': 0}

        for symbol in symbols:
            if len(results) >= max_results:
                break

            print(f"[{analyzed+1:3d}] {symbol:<12}", end=" ")

            # Fetch data
            data, status = self.fetch_stock_data(symbol)
            analyzed += 1

            if data is None:
                if "delisted" in status.lower() or "timezone" in status.lower():
                    errors['delisted'] += 1
                    print("❌ Delisted")
                elif "no data" in status.lower():
                    errors['no_data'] += 1
                    print("❌ No data")
                elif "invalid" in status.lower():
                    errors['invalid'] += 1
                    print("❌ Invalid")
                else:
                    errors['other'] += 1
                    print(f"❌ {status[:20]}")
                continue

            # Analyze for opportunity
            analysis = self.analyze_stock_for_rsi_opportunity(symbol, data)

            if analysis:
                # Get company info safely
                try:
                    ticker = yf.Ticker(f"{symbol}.NS")
                    info = ticker.info
                    analysis['company_name'] = info.get('longName', symbol)[:30]
                    analysis['sector'] = info.get('sector', 'Unknown')[:15]
                except:
                    analysis['company_name'] = symbol
                    analysis['sector'] = 'Unknown'

                results.append(analysis)
                print(f"✅ RSI:{analysis['current_rsi']:5.1f} Vol:{analysis['volume_ratio']:4.1f}x Score:{analysis['momentum_score']}/6")
            else:
                print("⚪ No opportunity")

            time.sleep(0.05)  # Rate limiting

        # Summary
        print(f"\nScan Summary:")
        print(f"  Analyzed: {analyzed}")
        print(f"  Opportunities: {len(results)}")
        print(f"  Errors - Delisted: {errors['delisted']}, No data: {errors['no_data']}, Invalid: {errors['invalid']}, Other: {errors['other']}")

        if results:
            return pd.DataFrame(results).sort_values(['momentum_score', 'current_rsi'], ascending=[False, True])
        else:
            return pd.DataFrame()

def main():
    """Main scanning function"""
    print("🔧 ROBUST RSI SCANNER - HANDLES DELISTED STOCKS")
    print("="*60)
    print("Features:")
    print("- Filters out known delisted/problematic stocks")
    print("- Handles timezone and data fetch errors gracefully")
    print("- RSI Range: 40-55, Volume: >1.1x, Positive momentum")
    print()

    scanner = RobustRSIScanner()

    csv_files = [
        ('nifty500.csv', 'NIFTY 500'),
        ('nifty500_banking.csv', 'BANKING'),
        ('nifty500_technology.csv', 'TECHNOLOGY'),
        ('nifty500_fmcg.csv', 'FMCG'),
        ('nifty500_pharmaceuticals.csv', 'PHARMA'),
    ]

    all_results = []

    for csv_file, title in csv_files:
        if os.path.exists(csv_file):
            results_df = scanner.scan_csv_for_opportunities(csv_file, max_results=10)

            if not results_df.empty:
                print(f"\n🎯 {title} OPPORTUNITIES:")
                print("-" * 50)
                for _, row in results_df.iterrows():
                    print(f"{row['symbol']:<12} RSI:{row['current_rsi']:5.1f} "
                          f"Vol:{row['volume_ratio']:4.1f}x Score:{row['momentum_score']}/6 "
                          f"Price:₹{row['current_price']:7.2f}")

                # Save results
                timestamp = datetime.now().strftime('%Y%m%d_%H%M')
                sector_name = csv_file.replace('nifty500_', '').replace('.csv', '').replace('nifty500', 'all')
                output_file = f"robust_rsi_{sector_name}_{timestamp}.csv"
                results_df.to_csv(output_file, index=False)
                print(f"💾 Saved to: {output_file}")

                all_results.append(results_df)
            else:
                print(f"\n❌ No opportunities found in {title}")

    # Combined results
    if all_results:
        combined_df = pd.concat(all_results, ignore_index=True)
        combined_sorted = combined_df.sort_values(['momentum_score', 'volume_ratio'], ascending=[False, False])

        print(f"\n{'='*70}")
        print("🏆 TOP OPPORTUNITIES ACROSS ALL SECTORS")
        print("="*70)

        for i, (_, row) in enumerate(combined_sorted.head(10).iterrows(), 1):
            print(f"{i:2d}. {row['symbol']:<12} | RSI: {row['current_rsi']:5.1f} | "
                  f"Vol: {row['volume_ratio']:4.1f}x | Score: {row['momentum_score']}/6")
            print(f"    Price: ₹{row['current_price']:8.2f} | Sector: {row['sector']}")

        # Save combined results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        combined_output = f"robust_rsi_all_sectors_{timestamp}.csv"
        combined_sorted.to_csv(combined_output, index=False)
        print(f"\n💾 All results saved to: {combined_output}")

        # High quality picks
        high_quality = combined_sorted[
            (combined_sorted['momentum_score'] >= 4) &
            (combined_sorted['volume_ratio'] > 1.2)
        ]

        if not high_quality.empty:
            print(f"\n🎯 HIGH QUALITY RECOMMENDATIONS:")
            print("-" * 40)
            for i, (_, row) in enumerate(high_quality.head(3).iterrows(), 1):
                rec = "STRONG BUY" if row['momentum_score'] >= 5 else "BUY"
                print(f"{i}. {row['symbol']} - {rec}")
                print(f"   RSI: {row['current_rsi']:.1f} → Target: 70")
                print(f"   Price: ₹{row['current_price']:.2f}")
                print(f"   Volume: {row['volume_ratio']:.1f}x average")
                print()

    else:
        print("\n❌ No opportunities found across all sectors")

    print(f"\n{'='*60}")
    print("✅ ROBUST SCAN COMPLETE - DELISTED STOCKS FILTERED")
    print("="*60)

if __name__ == "__main__":
    main()