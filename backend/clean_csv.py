#!/usr/bin/env python3
"""
Clean CSV Files - Remove Delisted/Problematic Stocks
====================================================
"""

import pandas as pd

def clean_nifty500_csv():
    """Clean the nifty500.csv file by removing problematic stocks"""

    # Known problematic stocks to remove
    blacklist = {
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

    try:
        # Read original CSV
        df = pd.read_csv('nifty500.csv')
        print(f"Original nifty500.csv: {len(df)} stocks")

        # Filter out blacklisted stocks
        clean_df = df[~df['Symbol'].isin(blacklist)]
        print(f"After cleaning: {len(clean_df)} stocks")
        print(f"Removed: {len(df) - len(clean_df)} problematic stocks")

        # Save cleaned version
        clean_df.to_csv('nifty500_clean.csv', index=False)
        print("✅ Saved as nifty500_clean.csv")

        # Show removed stocks
        removed_stocks = df[df['Symbol'].isin(blacklist)]['Symbol'].tolist()
        print(f"\nRemoved stocks: {', '.join(removed_stocks[:10])}...")

        return clean_df

    except FileNotFoundError:
        print("❌ nifty500.csv not found")
        return None

def main():
    print("🧹 CLEANING CSV FILES")
    print("=" * 40)
    print("Removing delisted and problematic stocks from CSV files")
    print()

    # Clean main nifty500 file
    clean_nifty500_csv()

    print(f"\n{'=' * 40}")
    print("✅ CSV CLEANING COMPLETE")
    print("Use 'nifty500_clean.csv' for future analyses to avoid errors")

if __name__ == "__main__":
    main()