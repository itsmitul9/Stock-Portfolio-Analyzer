import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Portfolio data
portfolio_data = {
    'Symbol': ['CDSL', 'CHENNPETRO', 'COCHINSHIP', 'ENGINERSIN', 'FACT', 'GSFC',
               'KALYANKJIL', 'MOIL', 'NETWEB', 'NOVAAGRI', 'PROTEAN', 'RITES', 'SCILAL'],
    'Health': [205, 547, 205, 558, 554, 744, 376, 560, 55, 538, 502, 558, 538],
    'Duration': [205, 547, 205, 558, 554, 744, 376, 560, 55, 538, 502, 558, 538],
    'Buy_Date': ['2025-06-23', '2024-07-16', '2025-06-23', '2024-07-05', '2024-07-09',
                 '2024-01-01', '2025-01-03', '2024-07-03', '2025-11-20', '2024-07-25',
                 '2024-08-30', '2024-07-05', '2024-07-25'],
    'Avg_Cost': [1723, 1209.98, 2230, 276.1, 1150.3, 275, 784.8, 530.5, 3481.80, 91.64, 2180, 381, 103.7],
    'Current_Price': [1419.9, 825.55, 1548.9, 193.88, 868.3, 173.45, 495.45, 340.4, 3273, 36.62, 710.9, 226.65, 46.44],
    'Quantity': [289, 312, 46, 90, 858, 384, 126, 1000, 117, 1111, 11, 264, 3000],
    'Capital_Gain_Type': ['STCG', 'LTCG', 'STCG', 'LTCG', 'LTCG', 'LTCG', 'LTCG', 'LTCG', 'STCG', 'LTCG', 'LTCG', 'LTCG', 'LTCG'],
    'Unrealized_PL_Pct': [-17.5914, -31.7716, -30.5426, -29.7791, -24.5155, -36.9273, -36.8693, -35.8341, -5.997, -60.0393, -67.3899, -40.5118, -55.2181]
}

# Create DataFrame
df = pd.DataFrame(portfolio_data)

# Calculate additional metrics
df['Investment_Value'] = df['Avg_Cost'] * df['Quantity']
df['Current_Value'] = df['Current_Price'] * df['Quantity']
df['Absolute_Loss'] = df['Current_Value'] - df['Investment_Value']
df['Loss_Amount'] = abs(df['Absolute_Loss'])

# Portfolio Summary
print("=" * 80)
print("PORTFOLIO HEALTH CHECK & RECOVERY ANALYSIS")
print("=" * 80)
print()

total_invested = df['Investment_Value'].sum()
total_current_value = df['Current_Value'].sum()
total_loss = total_invested - total_current_value
total_loss_pct = (total_loss / total_invested) * 100

print(f"PORTFOLIO OVERVIEW:")
print(f"Total Invested Amount: ₹{total_invested:,.2f}")
print(f"Current Portfolio Value: ₹{total_current_value:,.2f}")
print(f"Total Unrealized Loss: ₹{total_loss:,.2f}")
print(f"Overall Loss Percentage: {total_loss_pct:.2f}%")
print(f"Number of Positions: {len(df)}")
print()

# Loss categorization
severe_losses = df[df['Unrealized_PL_Pct'] <= -50]
high_losses = df[(df['Unrealized_PL_Pct'] > -50) & (df['Unrealized_PL_Pct'] <= -35)]
moderate_losses = df[(df['Unrealized_PL_Pct'] > -35) & (df['Unrealized_PL_Pct'] <= -20)]
minor_losses = df[df['Unrealized_PL_Pct'] > -20]

print("LOSS CATEGORIZATION:")
print(f"Severe Losses (>50%): {len(severe_losses)} stocks - ₹{severe_losses['Loss_Amount'].sum():,.2f}")
print(f"High Losses (35-50%): {len(high_losses)} stocks - ₹{high_losses['Loss_Amount'].sum():,.2f}")
print(f"Moderate Losses (20-35%): {len(moderate_losses)} stocks - ₹{moderate_losses['Loss_Amount'].sum():,.2f}")
print(f"Minor Losses (<20%): {len(minor_losses)} stocks - ₹{minor_losses['Loss_Amount'].sum():,.2f}")
print()

# Worst performers
print("TOP 5 WORST PERFORMERS:")
worst_performers = df.nsmallest(5, 'Unrealized_PL_Pct')
for _, stock in worst_performers.iterrows():
    print(f"{stock['Symbol']}: {stock['Unrealized_PL_Pct']:.2f}% (₹{stock['Loss_Amount']:,.0f} loss)")
print()

# Tax implications
ltcg_stocks = df[df['Capital_Gain_Type'] == 'LTCG']
stcg_stocks = df[df['Capital_Gain_Type'] == 'STCG']

print("TAX IMPLICATIONS:")
print(f"LTCG Eligible Stocks: {len(ltcg_stocks)} (10% tax on gains > ₹1L)")
print(f"STCG Stocks: {len(stcg_stocks)} (15% tax rate)")
print()

# Position sizing analysis
df['Position_Size_Pct'] = (df['Investment_Value'] / total_invested) * 100
large_positions = df[df['Position_Size_Pct'] > 15]

if len(large_positions) > 0:
    print("CONCENTRATION RISK:")
    print("Large positions (>15% of portfolio):")
    for _, stock in large_positions.iterrows():
        print(f"{stock['Symbol']}: {stock['Position_Size_Pct']:.1f}% of portfolio")
    print()

print("=" * 80)
print("RECOVERY STRATEGIES BY CATEGORY")
print("=" * 80)
print()

# Severe losses (>50%) - Consider exit
if len(severe_losses) > 0:
    print("🚨 SEVERE LOSSES (>50%) - IMMEDIATE ACTION REQUIRED:")
    for _, stock in severe_losses.iterrows():
        print(f"\n{stock['Symbol']} - Loss: {stock['Unrealized_PL_Pct']:.1f}%")
        print(f"   Current Investment: ₹{stock['Investment_Value']:,.0f}")
        print(f"   Current Value: ₹{stock['Current_Value']:,.0f}")
        print(f"   RECOMMENDATION: Strong consideration for exit")
        print(f"   REASON: Recovery to breakeven requires {abs(stock['Unrealized_PL_Pct'])/(100+stock['Unrealized_PL_Pct'])*100:.1f}% gain")
        if stock['Capital_Gain_Type'] == 'LTCG':
            print(f"   TAX BENEFIT: Can use this loss to offset future LTCG")

print()

# High losses (35-50%) - Evaluate fundamentals
if len(high_losses) > 0:
    print("⚠️  HIGH LOSSES (35-50%) - FUNDAMENTAL REVIEW:")
    for _, stock in high_losses.iterrows():
        required_gain = abs(stock['Unrealized_PL_Pct'])/(100+stock['Unrealized_PL_Pct'])*100
        print(f"\n{stock['Symbol']} - Loss: {stock['Unrealized_PL_Pct']:.1f}%")
        print(f"   Recovery requires: {required_gain:.1f}% gain")
        print(f"   STRATEGY: Detailed fundamental analysis required")
        print(f"   CONSIDER: Partial exit (50%) if no strong recovery thesis")

print()

# Recovery strategies
print("=" * 80)
print("SPECIFIC RECOVERY RECOMMENDATIONS")
print("=" * 80)
print()

print("1. IMMEDIATE ACTIONS (Next 30 days):")
print("   • Exit PROTEAN (-67.39%) and NOVAAGRI (-60.04%) - Cut severe losses")
print("   • Use tax loss harvesting benefits for future gains")
print("   • Review fundamental thesis for SCILAL (-55.22%)")
print()

print("2. MEDIUM-TERM STRATEGY (3-6 months):")
print("   • Evaluate high-loss positions (RITES, GSFC, KALYANKJIL) for recovery potential")
print("   • Consider averaging down ONLY if fundamental story is intact")
print("   • Set stop-loss at additional 10-15% decline for remaining positions")
print()

print("3. PORTFOLIO REBALANCING:")
print("   • Reduce position sizes to max 10-12% per stock")
print("   • Focus on quality stocks with strong fundamentals")
print("   • Consider sector diversification")
print()

print("4. RISK MANAGEMENT:")
print("   • Set target prices for remaining positions")
print("   • Use systematic approach: exit if additional 10% loss")
print("   • Don't average down on already heavy losers")
print()

# Calculate recovery scenarios
print("=" * 80)
print("RECOVERY SCENARIOS")
print("=" * 80)
print()

# If we exit worst 3 performers
worst_3 = df.nsmallest(3, 'Unrealized_PL_Pct')
remaining_portfolio_value = total_current_value - worst_3['Current_Value'].sum()
remaining_investment = total_invested - worst_3['Investment_Value'].sum()

print(f"SCENARIO 1: Exit worst 3 performers ({', '.join(worst_3['Symbol'].tolist())})")
print(f"Remaining portfolio value: ₹{remaining_portfolio_value:,.2f}")
print(f"Remaining investment: ₹{remaining_investment:,.2f}")
print(f"Reduced loss: ₹{worst_3['Loss_Amount'].sum():,.2f}")
print(f"New portfolio loss %: {((remaining_investment - remaining_portfolio_value)/remaining_investment)*100:.2f}%")
print()

print("SCENARIO 2: Partial exit (50%) from severe loss positions")
partial_exit_value = severe_losses['Current_Value'].sum() * 0.5
partial_recovery_needed = (total_invested - total_loss * 0.3) / total_current_value
print(f"If you exit 50% from severe losers and remaining portfolio gains 25%:")
print(f"Potential recovery: ₹{total_current_value * 0.25:,.2f}")
print()

# Final recommendations
print("=" * 80)
print("FINAL RECOMMENDATIONS")
print("=" * 80)
print()
print("PRIORITY 1 (This Week):")
print("🔴 Exit: PROTEAN, NOVAAGRI, SCILAL (Combined loss: ₹{:,.0f})".format(
    df[df['Symbol'].isin(['PROTEAN', 'NOVAAGRI', 'SCILAL'])]['Loss_Amount'].sum()))
print()
print("PRIORITY 2 (This Month):")
print("🟡 Review: RITES, GSFC, KALYANKJIL for fundamental strength")
print("🟡 Hold: NETWEB (smallest loss, good recovery potential)")
print()
print("PRIORITY 3 (Ongoing):")
print("🟢 Monitor: Remaining positions with 10% additional stop-loss")
print("🟢 Rebalance: Reduce concentration, improve diversification")
print()

# Save detailed analysis
df_detailed = df[['Symbol', 'Unrealized_PL_Pct', 'Loss_Amount', 'Investment_Value',
                  'Current_Value', 'Capital_Gain_Type', 'Position_Size_Pct']].copy()
df_detailed = df_detailed.sort_values('Unrealized_PL_Pct')

print("DETAILED POSITION ANALYSIS:")
print(df_detailed.to_string(index=False, float_format='%.2f'))