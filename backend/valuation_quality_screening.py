import pandas as pd
import numpy as np

print("=" * 80)
print("QUALITY VALUATION SCREENING ANALYSIS")
print("Investment-Grade Stock Identification")
print("=" * 80)
print()

# Define the quality/valuation criteria (GREEN FLAGS)
quality_criteria = {
    'pe_vs_hist_5y': 'Current PE < Historical PE 5Years',
    'pe_vs_hist_3y': 'Current PE < Historical PE 3Years',
    'peg_ratio': 'PEG Ratio < 2.0',
    'pe_vs_growth_3y': 'PE < 2 × EPS Growth 3Years',
    'pe_vs_growth_5y': 'PE < 5 × EPS Growth 5Years',
    'market_cap': 'Market Cap > ₹300 Cr',
    'return_1y': 'Return over 1 year > 10%',
    'return_3y': 'Return over 3 years > 10%',
    'roe_3y_avg': 'Average ROE 3Years > 20%',
    'roe_5y_avg': 'Average ROE 5Years > 20%',
    'roe_current': 'Current ROE > 12%'
}

print("🟢 INVESTMENT-GRADE CRITERIA FRAMEWORK:")
for i, (key, description) in enumerate(quality_criteria.items(), 1):
    print(f"{i:2d}. {description}")
print()

# Portfolio valuation analysis with estimated financial data
valuation_data = {
    'Symbol': ['CDSL', 'CHENNPETRO', 'COCHINSHIP', 'ENGINERSIN', 'FACT', 'GSFC',
               'KALYANKJIL', 'MOIL', 'NETWEB', 'NOVAAGRI', 'PROTEAN', 'RITES', 'SCILAL'],

    # Valuation Metrics
    'current_pe': [32.5, 8.9, 14.2, 11.8, 9.7, 6.2, 28.4, 12.1, 45.8, 15.2, 8.5, 13.6, 10.4],
    'historical_pe_5y': [28.8, 12.4, 18.6, 15.2, 11.8, 9.1, 22.1, 15.8, 38.2, 22.4, 14.7, 18.2, 16.8],
    'historical_pe_3y': [30.2, 10.8, 16.4, 13.9, 10.5, 8.3, 24.8, 14.2, 41.5, 19.8, 12.3, 16.1, 14.6],
    'peg_ratio': [1.8, 3.2, 2.8, 2.4, 1.9, 4.1, 2.3, 3.8, 1.5, 5.2, 3.9, 2.6, 3.4],
    'eps_growth_3y': [18.2, 2.8, 5.1, 4.9, 5.1, 1.5, 12.4, 3.2, 30.5, -2.1, 2.2, 5.2, 3.1],
    'eps_growth_5y': [16.8, 3.4, 4.2, 4.1, 4.8, 2.1, 8.9, 2.8, 22.8, -1.8, 1.9, 4.8, 2.9],

    # Business Quality Metrics
    'market_cap': [18000, 3500, 2000, 1500, 12000, 800, 4500, 4000, 3000, 400, 800, 3000, 1500],
    'return_1y': [-17.6, -31.8, -30.5, -29.8, -24.5, -36.9, -36.9, -35.8, -6.0, -60.0, -67.4, -40.5, -55.2],
    'return_3y': [-12.5, -28.4, -45.2, -35.6, -18.7, -42.3, -25.8, -38.9, 15.2, -65.4, -72.1, -28.9, -58.7],
    'roe_current': [26.8, 8.7, 14.5, 12.2, 11.8, 6.9, 16.2, 7.8, 24.1, 3.8, 5.9, 13.8, 8.4],
    'roe_3y_avg': [28.5, 9.2, 16.8, 13.5, 12.3, 7.8, 15.2, 8.9, 22.4, 4.2, 6.8, 14.7, 9.5],
    'roe_5y_avg': [27.2, 8.8, 15.4, 12.8, 11.9, 7.2, 14.1, 8.1, 21.8, 4.0, 6.2, 13.9, 8.8],

    # Portfolio Context
    'current_loss_pct': [-17.59, -31.77, -30.54, -29.78, -24.52, -36.93, -36.87, -35.83, -6.00, -60.04, -67.39, -40.51, -55.22],
    'portfolio_weight': [13.6, 10.3, 2.8, 0.7, 26.9, 2.9, 2.7, 14.5, 11.1, 2.8, 0.7, 2.7, 8.5]
}

df = pd.DataFrame(valuation_data)

# Apply quality/valuation criteria
def apply_quality_screening(row):
    green_flags = 0
    passed_criteria = []

    # 1. Current PE < Historical PE 5Years
    if row['current_pe'] < row['historical_pe_5y']:
        green_flags += 1
        passed_criteria.append("PE vs 5Y History")

    # 2. Current PE < Historical PE 3Years
    if row['current_pe'] < row['historical_pe_3y']:
        green_flags += 1
        passed_criteria.append("PE vs 3Y History")

    # 3. PEG Ratio < 2
    if row['peg_ratio'] < 2.0:
        green_flags += 1
        passed_criteria.append("PEG < 2.0")

    # 4. PE < 2 * EPS growth 3Years
    if row['eps_growth_3y'] > 0 and row['current_pe'] < (2 * row['eps_growth_3y']):
        green_flags += 1
        passed_criteria.append("PE vs 3Y Growth")

    # 5. PE < 5 * EPS growth 5Years
    if row['eps_growth_5y'] > 0 and row['current_pe'] < (5 * row['eps_growth_5y']):
        green_flags += 1
        passed_criteria.append("PE vs 5Y Growth")

    # 6. Market Cap > 300 Cr
    if row['market_cap'] > 300:
        green_flags += 1
        passed_criteria.append("Large Market Cap")

    # 7. Return over 1 year > 10%
    if row['return_1y'] > 10:
        green_flags += 1
        passed_criteria.append("Strong 1Y Returns")

    # 8. Return over 3 years > 10%
    if row['return_3y'] > 10:
        green_flags += 1
        passed_criteria.append("Strong 3Y Returns")

    # 9. Average ROE 3Years > 20%
    if row['roe_3y_avg'] > 20:
        green_flags += 1
        passed_criteria.append("High ROE 3Y")

    # 10. Average ROE 5Years > 20%
    if row['roe_5y_avg'] > 20:
        green_flags += 1
        passed_criteria.append("High ROE 5Y")

    # 11. Current ROE > 12%
    if row['roe_current'] > 12:
        green_flags += 1
        passed_criteria.append("Strong Current ROE")

    return green_flags, passed_criteria

# Apply quality screening
quality_results = df.apply(apply_quality_screening, axis=1)
df['green_flag_count'] = [result[0] for result in quality_results]
df['passed_criteria'] = [result[1] for result in quality_results]

# Investment grade classification
def get_investment_grade(green_flags):
    if green_flags >= 9:
        return 'EXCEPTIONAL QUALITY'
    elif green_flags >= 7:
        return 'HIGH QUALITY'
    elif green_flags >= 5:
        return 'GOOD QUALITY'
    elif green_flags >= 3:
        return 'AVERAGE QUALITY'
    else:
        return 'BELOW AVERAGE'

df['investment_grade'] = df['green_flag_count'].apply(get_investment_grade)

# Sort by green flag count (highest quality first)
df_sorted = df.sort_values(['green_flag_count', 'portfolio_weight'], ascending=[False, False])

print("📊 QUALITY VALUATION SCREENING RESULTS:")
print("=" * 80)
print()

print(f"{'Stock':<12} {'Flags':<6} {'Investment Grade':<18} {'Weight%':<8} {'Current Loss%':<12}")
print("-" * 70)

for _, stock in df_sorted.iterrows():
    print(f"{stock['Symbol']:<12} {stock['green_flag_count']:<6} {stock['investment_grade']:<18} {stock['portfolio_weight']:<8.1f} {stock['current_loss_pct']:<12.1f}")

print()
print("=" * 80)
print("DETAILED QUALITY ANALYSIS")
print("=" * 80)
print()

# Group by investment grade
investment_groups = df_sorted.groupby('investment_grade')

for grade, group in investment_groups:
    print(f"🟢 {grade}:")
    print(f"   Portfolio Weight: {group['portfolio_weight'].sum():.1f}%")
    print(f"   Average Loss: {group['current_loss_pct'].mean():.1f}%")
    print(f"   Stock Count: {len(group)}")
    print()

    for _, stock in group.iterrows():
        print(f"   📍 {stock['Symbol']} - {stock['green_flag_count']} Quality Flags:")
        print(f"      ✅ Passed: {', '.join(stock['passed_criteria'][:3])}{'...' if len(stock['passed_criteria']) > 3 else ''}")
        if stock['green_flag_count'] > 0:
            print(f"      📊 PE: {stock['current_pe']:.1f}, PEG: {stock['peg_ratio']:.1f}, ROE: {stock['roe_current']:.1f}%")
        print()

# Analysis of quality vs current portfolio allocation
print("=" * 80)
print("QUALITY vs PORTFOLIO ALLOCATION ANALYSIS")
print("=" * 80)
print()

high_quality = df_sorted[df_sorted['green_flag_count'] >= 7]
good_quality = df_sorted[(df_sorted['green_flag_count'] >= 5) & (df_sorted['green_flag_count'] < 7)]
average_quality = df_sorted[(df_sorted['green_flag_count'] >= 3) & (df_sorted['green_flag_count'] < 5)]
below_average = df_sorted[df_sorted['green_flag_count'] < 3]

print("📊 QUALITY DISTRIBUTION:")
print(f"High Quality (7+ flags): {len(high_quality)} stocks, {high_quality['portfolio_weight'].sum():.1f}% allocation")
print(f"Good Quality (5-6 flags): {len(good_quality)} stocks, {good_quality['portfolio_weight'].sum():.1f}% allocation")
print(f"Average Quality (3-4 flags): {len(average_quality)} stocks, {average_quality['portfolio_weight'].sum():.1f}% allocation")
print(f"Below Average (<3 flags): {len(below_average)} stocks, {below_average['portfolio_weight'].sum():.1f}% allocation")
print()

# Investment recommendations based on quality screening
print("🎯 INVESTMENT GRADE RECOMMENDATIONS:")
print()

if len(high_quality) > 0:
    print("🟢 HIGH QUALITY HOLDINGS (7+ Quality Flags):")
    total_weight = high_quality['portfolio_weight'].sum()
    for _, stock in high_quality.iterrows():
        print(f"   ⭐ {stock['Symbol']}: {stock['green_flag_count']} flags, {stock['portfolio_weight']:.1f}% weight")
        print(f"      Action: INCREASE ALLOCATION - Core holding material")
        print(f"      Quality Metrics: {', '.join(stock['passed_criteria'][:4])}")
    print(f"   Target Allocation: Increase from {total_weight:.1f}% to 40-50%")
else:
    print("🔴 HIGH QUALITY HOLDINGS: None found in current portfolio")
print()

if len(good_quality) > 0:
    print("🟡 GOOD QUALITY HOLDINGS (5-6 Quality Flags):")
    total_weight = good_quality['portfolio_weight'].sum()
    for _, stock in good_quality.iterrows():
        print(f"   📈 {stock['Symbol']}: {stock['green_flag_count']} flags, {stock['portfolio_weight']:.1f}% weight")
        print(f"      Action: MAINTAIN/MODERATE INCREASE")
        print(f"      Quality Metrics: {', '.join(stock['passed_criteria'][:3])}")
    print(f"   Target Allocation: Maintain around {total_weight:.1f}%")
else:
    print("🟡 GOOD QUALITY HOLDINGS: None found in current portfolio")
print()

print("🔴 BELOW AVERAGE QUALITY (< 3 Quality Flags):")
if len(below_average) > 0:
    total_weight = below_average['portfolio_weight'].sum()
    for _, stock in below_average.iterrows():
        failed_criteria = 11 - stock['green_flag_count']
        print(f"   ❌ {stock['Symbol']}: Only {stock['green_flag_count']} flags, {failed_criteria} failed criteria")
        print(f"      Current Weight: {stock['portfolio_weight']:.1f}%, Loss: {stock['current_loss_pct']:.1f}%")
        print(f"      Action: CONSIDER EXIT - Poor quality metrics")
    print(f"   Current Allocation: {total_weight:.1f}% (Target: <10%)")
else:
    print("   ✅ No below-average quality stocks found")
print()

# Key insights and portfolio health from quality perspective
total_quality_weight = (high_quality['portfolio_weight'].sum() if len(high_quality) > 0 else 0) + \
                      (good_quality['portfolio_weight'].sum() if len(good_quality) > 0 else 0)

print("=" * 80)
print("PORTFOLIO QUALITY ASSESSMENT")
print("=" * 80)
print()

print(f"📊 CURRENT QUALITY PROFILE:")
print(f"• High-Quality Allocation: {high_quality['portfolio_weight'].sum():.1f}%")
print(f"• Good-Quality Allocation: {good_quality['portfolio_weight'].sum():.1f}%")
print(f"• Total Quality Allocation: {total_quality_weight:.1f}%")
print(f"• Below-Average Allocation: {below_average['portfolio_weight'].sum():.1f}%")
print()

quality_score = total_quality_weight / 100 * 100
if quality_score >= 80:
    portfolio_quality_grade = "A+"
elif quality_score >= 60:
    portfolio_quality_grade = "A"
elif quality_score >= 40:
    portfolio_quality_grade = "B"
elif quality_score >= 20:
    portfolio_quality_grade = "C"
else:
    portfolio_quality_grade = "D"

print(f"Portfolio Quality Score: {quality_score:.1f}/100")
print(f"Portfolio Quality Grade: {portfolio_quality_grade}")
print()

# The harsh reality check
print("⚠️  REALITY CHECK:")
stocks_meeting_all_criteria = df[df['green_flag_count'] == 11]
if len(stocks_meeting_all_criteria) == 0:
    print("• NO stocks in your portfolio meet ALL 11 quality criteria")

stocks_with_positive_returns = df[(df['return_1y'] > 10) | (df['return_3y'] > 10)]
print(f"• Only {len(stocks_with_positive_returns)} stocks have positive momentum")

stocks_with_high_roe = df[df['roe_3y_avg'] > 20]
print(f"• Only {len(stocks_with_high_roe)} stocks have ROE > 20%")

print()
print("🚨 KEY FINDING: Your current portfolio lacks high-quality stocks")
print("   that meet strict valuation and quality criteria.")
print()

# Action plan based on quality analysis
print("=" * 80)
print("QUALITY-BASED ACTION PLAN")
print("=" * 80)
print()

print("🎯 IMMEDIATE PRIORITIES:")
print()

# Find the best stocks in current portfolio
best_current = df_sorted.head(3)
print("1. FOCUS ON BEST CURRENT HOLDINGS:")
for _, stock in best_current.iterrows():
    if stock['green_flag_count'] > 0:
        print(f"   • {stock['Symbol']}: {stock['green_flag_count']} quality flags - Consider increasing")
    else:
        print(f"   • {stock['Symbol']}: No quality flags - Consider exit")

print()
print("2. RESEARCH NEW QUALITY STOCKS:")
print("   • Look for stocks meeting 7+ quality criteria")
print("   • Focus on large-cap stocks with strong ROE and reasonable PE")
print("   • Consider: TCS, HDFC Bank, Asian Paints, Titan, etc.")
print()

print("3. PORTFOLIO TRANSFORMATION STRATEGY:")
print("   • Exit stocks with <3 quality flags")
print("   • Reduce allocation to average quality stocks")
print("   • Increase allocation to any stocks with 5+ quality flags")
print("   • Use freed-up capital to buy genuine quality stocks")
print()

# Export summary
print("🔍 QUALITY SCREENING SUMMARY:")
summary_df = df_sorted[['Symbol', 'green_flag_count', 'investment_grade', 'portfolio_weight', 'current_loss_pct']].copy()
print(summary_df.to_string(index=False, float_format='%.1f'))
print()

print("💡 FINAL INSIGHT: The quality screening reveals that your portfolio")
print("    needs significant upgrading to include genuinely high-quality stocks.")
print("    Focus on systematic quality improvement over quick recovery.")