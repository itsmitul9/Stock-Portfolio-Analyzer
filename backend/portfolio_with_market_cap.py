import pandas as pd

# Portfolio data with sector and market cap classification
portfolio_detailed = {
    'Symbol': ['CDSL', 'CHENNPETRO', 'COCHINSHIP', 'ENGINERSIN', 'FACT', 'GSFC',
               'KALYANKJIL', 'MOIL', 'NETWEB', 'NOVAAGRI', 'PROTEAN', 'RITES', 'SCILAL'],
    'Sector': ['Financial Services', 'Oil & Gas', 'Capital Goods', 'Capital Goods',
               'Chemicals', 'Chemicals', 'Consumer Discretionary', 'Metals & Mining',
               'Technology', 'Agriculture', 'Technology/Services', 'Capital Goods', 'Pharmaceuticals'],
    'Market_Cap': ['Large Cap', 'Mid Cap', 'Small Cap', 'Small Cap', 'Large Cap', 'Small Cap',
                   'Small Cap', 'Mid Cap', 'Small Cap', 'Small Cap', 'Small Cap', 'Mid Cap', 'Small Cap'],
    'Current_Price': [1419.9, 825.55, 1548.9, 193.88, 868.3, 173.45, 495.45, 340.4, 3273, 36.62, 710.9, 226.65, 46.44],
    'Avg_Cost': [1723, 1209.98, 2230, 276.1, 1150.3, 275, 784.8, 530.5, 3481.80, 91.64, 2180, 381, 103.7],
    'Quantity': [289, 312, 46, 90, 858, 384, 126, 1000, 117, 1111, 11, 264, 3000],
    'Investment_Value': [497947, 377513.76, 102580, 24849, 986957.4, 105600, 98884.8, 530500, 407370.6, 101812.04, 23980, 100584, 311100],
    'Current_Value': [410351.1, 257571.6, 71249.4, 17449.2, 745001.4, 66604.8, 62426.7, 340400, 382941, 40684.82, 7819.9, 59835.6, 139320],
    'Unrealized_PL_Pct': [-17.59, -31.77, -30.54, -29.78, -24.52, -36.93, -36.87, -35.83, -6.00, -60.04, -67.39, -40.51, -55.22],
    'Capital_Gain_Type': ['STCG', 'LTCG', 'STCG', 'LTCG', 'LTCG', 'LTCG', 'LTCG', 'LTCG', 'STCG', 'LTCG', 'LTCG', 'LTCG', 'LTCG']
}

# Market cap ranges (approximate as of 2024-25)
market_cap_criteria = {
    'Large Cap': 'Market Cap > ₹20,000 Cr',
    'Mid Cap': 'Market Cap ₹5,000-20,000 Cr',
    'Small Cap': 'Market Cap < ₹5,000 Cr'
}

df = pd.DataFrame(portfolio_detailed)
df['Loss_Amount'] = df['Investment_Value'] - df['Current_Value']
df['Position_Size_Pct'] = (df['Investment_Value'] / df['Investment_Value'].sum()) * 100

print("=" * 80)
print("PORTFOLIO ANALYSIS: SECTOR & MARKET CAP CLASSIFICATION")
print("=" * 80)
print()

# Market cap breakdown
print("📊 MARKET CAP DISTRIBUTION:")
market_cap_summary = df.groupby('Market_Cap').agg({
    'Investment_Value': 'sum',
    'Current_Value': 'sum',
    'Loss_Amount': 'sum',
    'Symbol': 'count'
}).reset_index()
market_cap_summary.columns = ['Market_Cap', 'Investment', 'Current_Value', 'Loss_Amount', 'Stock_Count']
market_cap_summary['Portfolio_Weight'] = (market_cap_summary['Investment'] / market_cap_summary['Investment'].sum()) * 100
market_cap_summary['Loss_Pct'] = (market_cap_summary['Loss_Amount'] / market_cap_summary['Investment']) * 100

for _, row in market_cap_summary.iterrows():
    print(f"{row['Market_Cap']}: {row['Stock_Count']} stocks, {row['Portfolio_Weight']:.1f}% allocation, {row['Loss_Pct']:.1f}% loss")
print()

# Sector breakdown
print("🏭 SECTOR DISTRIBUTION:")
sector_summary = df.groupby('Sector').agg({
    'Investment_Value': 'sum',
    'Current_Value': 'sum',
    'Loss_Amount': 'sum',
    'Symbol': 'count'
}).reset_index()
sector_summary.columns = ['Sector', 'Investment', 'Current_Value', 'Loss_Amount', 'Stock_Count']
sector_summary['Portfolio_Weight'] = (sector_summary['Investment'] / sector_summary['Investment'].sum()) * 100
sector_summary['Loss_Pct'] = (sector_summary['Loss_Amount'] / sector_summary['Investment']) * 100
sector_summary = sector_summary.sort_values('Portfolio_Weight', ascending=False)

for _, row in sector_summary.iterrows():
    print(f"{row['Sector']}: {row['Portfolio_Weight']:.1f}% allocation, {row['Loss_Pct']:.1f}% loss")
print()

# Detailed stock analysis
print("=" * 80)
print("DETAILED STOCK ANALYSIS")
print("=" * 80)
print()

# Sort by loss percentage for analysis
df_sorted = df.sort_values('Unrealized_PL_Pct').reset_index(drop=True)

print(f"{'Stock':<12} {'Sector':<20} {'Cap':<10} {'Loss%':<8} {'₹Loss':<12} {'Action':<15}")
print("-" * 80)

# Define actions based on previous analysis
actions = {
    'PROTEAN': 'EXIT NOW',
    'NOVAAGRI': 'EXIT NOW',
    'SCILAL': 'EXIT NOW',
    'RITES': 'MONITOR',
    'GSFC': 'PARTIAL EXIT',
    'KALYANKJIL': 'PARTIAL EXIT',
    'MOIL': 'PARTIAL EXIT',
    'CHENNPETRO': 'MONITOR',
    'COCHINSHIP': 'MONITOR',
    'ENGINERSIN': 'MONITOR',
    'FACT': 'REDUCE SIZE',
    'CDSL': 'HOLD',
    'NETWEB': 'HOLD'
}

for _, stock in df_sorted.iterrows():
    action = actions.get(stock['Symbol'], 'REVIEW')
    loss_amount = f"₹{stock['Loss_Amount']:,.0f}"
    print(f"{stock['Symbol']:<12} {stock['Sector']:<20} {stock['Market_Cap']:<10} {stock['Unrealized_PL_Pct']:>6.1f}% {loss_amount:<12} {action:<15}")

print()

# Risk analysis by market cap
print("⚠️  RISK ANALYSIS BY MARKET CAP:")
print()

small_cap_stocks = df[df['Market_Cap'] == 'Small Cap']
mid_cap_stocks = df[df['Market_Cap'] == 'Mid Cap']
large_cap_stocks = df[df['Market_Cap'] == 'Large Cap']

print(f"Small Cap Risk:")
print(f"• {len(small_cap_stocks)} stocks ({(small_cap_stocks['Investment_Value'].sum()/df['Investment_Value'].sum()*100):.1f}% of portfolio)")
print(f"• Average loss: {small_cap_stocks['Unrealized_PL_Pct'].mean():.1f}%")
print(f"• Highest volatility and recovery uncertainty")
print(f"• Recommendation: Reduce exposure to <30% of portfolio")
print()

print(f"Mid Cap Performance:")
print(f"• {len(mid_cap_stocks)} stocks ({(mid_cap_stocks['Investment_Value'].sum()/df['Investment_Value'].sum()*100):.1f}% of portfolio)")
print(f"• Average loss: {mid_cap_stocks['Unrealized_PL_Pct'].mean():.1f}%")
print(f"• Moderate risk-reward profile")
print()

print(f"Large Cap Stability:")
print(f"• {len(large_cap_stocks)} stocks ({(large_cap_stocks['Investment_Value'].sum()/df['Investment_Value'].sum()*100):.1f}% of portfolio)")
print(f"• Average loss: {large_cap_stocks['Unrealized_PL_Pct'].mean():.1f}%")
print(f"• Lower volatility, better recovery potential")
print(f"• Recommendation: Increase allocation to >50% of portfolio")
print()

# Rebalancing recommendations
print("🎯 REBALANCING RECOMMENDATIONS:")
print()
print("Current Allocation:")
for cap_type in ['Large Cap', 'Mid Cap', 'Small Cap']:
    weight = market_cap_summary[market_cap_summary['Market_Cap'] == cap_type]['Portfolio_Weight'].iloc[0]
    print(f"• {cap_type}: {weight:.1f}%")

print()
print("Target Allocation (Post-Recovery):")
print("• Large Cap: 60-70% (Quality, Stability)")
print("• Mid Cap: 20-25% (Growth Potential)")
print("• Small Cap: 10-15% (High Growth, High Risk)")
print()

# Sector concentration analysis
print("🏭 SECTOR CONCENTRATION CONCERNS:")
print()
over_concentrated = sector_summary[sector_summary['Portfolio_Weight'] > 15]
for _, sector in over_concentrated.iterrows():
    print(f"⚠️  {sector['Sector']}: {sector['Portfolio_Weight']:.1f}% (Reduce to <15%)")

print()
print("Target Sector Allocation:")
print("• No single sector >15% of portfolio")
print("• Maximum 3-4 sectors with >10% allocation")
print("• Diversify across cyclical and defensive sectors")
print()

# Export summary
summary_export = df[['Symbol', 'Sector', 'Market_Cap', 'Unrealized_PL_Pct', 'Loss_Amount', 'Position_Size_Pct']].copy()
summary_export['Action'] = summary_export['Symbol'].map(actions)
summary_export = summary_export.sort_values('Unrealized_PL_Pct')

print("=" * 80)
print("PORTFOLIO SUMMARY FOR EXPORT")
print("=" * 80)
print()
print(summary_export.to_string(index=False, float_format='%.2f'))

print()
print("💾 ANALYSIS SAVED TO FILES:")
print("• portfolio_analysis.py - Main portfolio analysis")
print("• sector_analysis.py - Sector-wise strategies")
print("• final_recommendations.py - Recovery action plan")
print("• portfolio_with_market_cap.py - This detailed analysis")
print()
print("📁 All files saved in: /Users/mitul/algo/")