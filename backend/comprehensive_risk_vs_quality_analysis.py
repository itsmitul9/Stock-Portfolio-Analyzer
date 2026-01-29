import pandas as pd
import numpy as np

print("=" * 80)
print("COMPREHENSIVE RISK vs QUALITY MATRIX ANALYSIS")
print("Complete Portfolio Assessment Framework")
print("=" * 80)
print()

# Combined data from both analyses
portfolio_matrix = {
    'Symbol': ['CDSL', 'CHENNPETRO', 'COCHINSHIP', 'ENGINERSIN', 'FACT', 'GSFC',
               'KALYANKJIL', 'MOIL', 'NETWEB', 'NOVAAGRI', 'PROTEAN', 'RITES', 'SCILAL'],

    # Risk Analysis Results (from checkpoint analysis)
    'red_flags': [2, 3, 3, 2, 2, 5, 3, 3, 2, 7, 5, 2, 6],
    'risk_category': ['MEDIUM RISK', 'MEDIUM-HIGH RISK', 'MEDIUM-HIGH RISK', 'MEDIUM RISK',
                     'MEDIUM RISK', 'EXTREMELY HIGH RISK', 'MEDIUM-HIGH RISK', 'MEDIUM-HIGH RISK',
                     'MEDIUM RISK', 'EXTREMELY HIGH RISK', 'EXTREMELY HIGH RISK', 'MEDIUM RISK',
                     'EXTREMELY HIGH RISK'],

    # Quality Analysis Results (from valuation screening)
    'green_flags': [7, 4, 5, 5, 6, 4, 3, 4, 8, 3, 4, 5, 4],
    'quality_grade': ['HIGH QUALITY', 'AVERAGE QUALITY', 'GOOD QUALITY', 'GOOD QUALITY',
                     'GOOD QUALITY', 'AVERAGE QUALITY', 'AVERAGE QUALITY', 'AVERAGE QUALITY',
                     'HIGH QUALITY', 'AVERAGE QUALITY', 'AVERAGE QUALITY', 'GOOD QUALITY',
                     'AVERAGE QUALITY'],

    # Portfolio Context
    'portfolio_weight': [13.6, 10.3, 2.8, 0.7, 26.9, 2.9, 2.7, 14.5, 11.1, 2.8, 0.7, 2.7, 8.5],
    'current_loss': [-17.6, -31.8, -30.5, -29.8, -24.5, -36.9, -36.9, -35.8, -6.0, -60.0, -67.4, -40.5, -55.2]
}

df = pd.DataFrame(portfolio_matrix)

# Create risk-quality matrix classification
def classify_stock(row):
    risk_score = row['red_flags']  # Higher = worse
    quality_score = row['green_flags']  # Higher = better

    if risk_score >= 5:  # High risk
        if quality_score >= 7:
            return 'HIGH_RISK_HIGH_QUALITY'  # Turnaround candidate
        elif quality_score >= 5:
            return 'HIGH_RISK_MEDIUM_QUALITY'  # Risky but some merit
        else:
            return 'HIGH_RISK_LOW_QUALITY'  # Avoid completely

    elif risk_score >= 3:  # Medium risk
        if quality_score >= 7:
            return 'MEDIUM_RISK_HIGH_QUALITY'  # Good opportunity
        elif quality_score >= 5:
            return 'MEDIUM_RISK_MEDIUM_QUALITY'  # Acceptable
        else:
            return 'MEDIUM_RISK_LOW_QUALITY'  # Below par

    else:  # Low risk (≤2 red flags)
        if quality_score >= 7:
            return 'LOW_RISK_HIGH_QUALITY'  # Ideal holdings
        elif quality_score >= 5:
            return 'LOW_RISK_MEDIUM_QUALITY'  # Solid holdings
        else:
            return 'LOW_RISK_LOW_QUALITY'  # Conservative but poor

df['matrix_classification'] = df.apply(classify_stock, axis=1)

# Investment action based on matrix position
def get_investment_action(classification):
    actions = {
        'LOW_RISK_HIGH_QUALITY': 'STRONG BUY/INCREASE',
        'LOW_RISK_MEDIUM_QUALITY': 'BUY/HOLD',
        'LOW_RISK_LOW_QUALITY': 'HOLD/REVIEW',
        'MEDIUM_RISK_HIGH_QUALITY': 'CONDITIONAL BUY',
        'MEDIUM_RISK_MEDIUM_QUALITY': 'HOLD/MONITOR',
        'MEDIUM_RISK_LOW_QUALITY': 'REDUCE/EXIT',
        'HIGH_RISK_HIGH_QUALITY': 'TURNAROUND PLAY',
        'HIGH_RISK_MEDIUM_QUALITY': 'HIGH RISK/REDUCE',
        'HIGH_RISK_LOW_QUALITY': 'IMMEDIATE EXIT'
    }
    return actions.get(classification, 'REVIEW')

df['recommended_action'] = df['matrix_classification'].apply(get_investment_action)

print("📊 RISK-QUALITY MATRIX RESULTS:")
print("=" * 80)
print()

# Sort by matrix classification priority (best first)
priority_order = ['LOW_RISK_HIGH_QUALITY', 'LOW_RISK_MEDIUM_QUALITY', 'MEDIUM_RISK_HIGH_QUALITY',
                 'MEDIUM_RISK_MEDIUM_QUALITY', 'LOW_RISK_LOW_QUALITY', 'MEDIUM_RISK_LOW_QUALITY',
                 'HIGH_RISK_HIGH_QUALITY', 'HIGH_RISK_MEDIUM_QUALITY', 'HIGH_RISK_LOW_QUALITY']

print(f"{'Stock':<12} {'Risk':<8} {'Quality':<8} {'Classification':<25} {'Weight%':<8} {'Action':<15}")
print("-" * 90)

for classification in priority_order:
    group = df[df['matrix_classification'] == classification]
    for _, stock in group.iterrows():
        risk_flags = f"{stock['red_flags']}R"
        quality_flags = f"{stock['green_flags']}Q"
        class_short = stock['matrix_classification'].replace('_', ' ')[:20]
        print(f"{stock['Symbol']:<12} {risk_flags:<8} {quality_flags:<8} {class_short:<25} {stock['portfolio_weight']:<8.1f} {stock['recommended_action']:<15}")

print()
print("=" * 80)
print("DETAILED MATRIX ANALYSIS")
print("=" * 80)
print()

# Group by matrix classification
matrix_groups = df.groupby('matrix_classification')

for classification, group in matrix_groups:
    class_display = classification.replace('_', ' ')
    total_weight = group['portfolio_weight'].sum()
    avg_loss = group['current_loss'].mean()

    print(f"📊 {class_display}:")
    print(f"   Portfolio Weight: {total_weight:.1f}%")
    print(f"   Average Loss: {avg_loss:.1f}%")
    print(f"   Stock Count: {len(group)}")
    print()

    for _, stock in group.iterrows():
        print(f"   🔘 {stock['Symbol']}: {stock['red_flags']} risk flags, {stock['green_flags']} quality flags")
        print(f"      Weight: {stock['portfolio_weight']:.1f}%, Loss: {stock['current_loss']:.1f}%")
        print(f"      Action: {stock['recommended_action']}")
        print()

# Portfolio transformation roadmap
print("=" * 80)
print("PORTFOLIO TRANSFORMATION ROADMAP")
print("=" * 80)
print()

# Calculate current allocation by matrix quadrant
ideal_stocks = df[df['matrix_classification'].str.contains('LOW_RISK_HIGH_QUALITY')]
good_stocks = df[df['matrix_classification'].str.contains('LOW_RISK_MEDIUM_QUALITY|MEDIUM_RISK_HIGH_QUALITY')]
acceptable_stocks = df[df['matrix_classification'].str.contains('MEDIUM_RISK_MEDIUM_QUALITY')]
problematic_stocks = df[df['matrix_classification'].str.contains('HIGH_RISK|LOW_QUALITY')]

print("🎯 CURRENT vs TARGET ALLOCATION:")
print()

current_ideal = ideal_stocks['portfolio_weight'].sum()
current_good = good_stocks['portfolio_weight'].sum()
current_acceptable = acceptable_stocks['portfolio_weight'].sum()
current_problematic = problematic_stocks['portfolio_weight'].sum()

print(f"Ideal Holdings (Low Risk + High Quality):")
print(f"   Current: {current_ideal:.1f}% | Target: 40-50%")
print(f"   Stocks: {', '.join(ideal_stocks['Symbol'].tolist()) if len(ideal_stocks) > 0 else 'None'}")
print()

print(f"Good Holdings (Low Risk + Med Quality OR Med Risk + High Quality):")
print(f"   Current: {current_good:.1f}% | Target: 30-40%")
print(f"   Stocks: {', '.join(good_stocks['Symbol'].tolist()) if len(good_stocks) > 0 else 'None'}")
print()

print(f"Acceptable Holdings (Medium Risk + Medium Quality):")
print(f"   Current: {current_acceptable:.1f}% | Target: 15-20%")
print(f"   Stocks: {', '.join(acceptable_stocks['Symbol'].tolist()) if len(acceptable_stocks) > 0 else 'None'}")
print()

print(f"Problematic Holdings (High Risk OR Low Quality):")
print(f"   Current: {current_problematic:.1f}% | Target: <10%")
print(f"   Stocks: {', '.join(problematic_stocks['Symbol'].tolist())}")
print()

# Phase-wise transformation plan
print("📅 TRANSFORMATION PHASES:")
print()

print("🔴 PHASE 1 - IMMEDIATE EXITS (Week 1-2):")
immediate_exits = df[df['matrix_classification'] == 'HIGH_RISK_LOW_QUALITY']
if len(immediate_exits) > 0:
    total_exit_weight = immediate_exits['portfolio_weight'].sum()
    print(f"   Exit stocks with high risk + low quality ({total_exit_weight:.1f}% of portfolio):")
    for _, stock in immediate_exits.iterrows():
        print(f"   ❌ {stock['Symbol']}: {stock['red_flags']} risk flags, {stock['green_flags']} quality flags")
        print(f"      Reason: Multiple structural issues, poor valuation metrics")
else:
    print("   ✅ No immediate exits required based on matrix analysis")

print()
print("🟡 PHASE 2 - HIGH RISK REDUCTION (Week 3-4):")
high_risk_stocks = df[df['red_flags'] >= 5]
if len(high_risk_stocks) > 0:
    print(f"   Reduce/exit high-risk positions:")
    for _, stock in high_risk_stocks.iterrows():
        if stock['green_flags'] >= 5:
            print(f"   📉 {stock['Symbol']}: High risk but some quality - Reduce by 50-70%")
        else:
            print(f"   ❌ {stock['Symbol']}: High risk, low quality - Complete exit")
else:
    print("   ✅ No high-risk positions to address")

print()
print("🟢 PHASE 3 - QUALITY CONCENTRATION (Month 2-3):")
quality_stocks = df[df['green_flags'] >= 7]
if len(quality_stocks) > 0:
    print(f"   Increase allocation to high-quality stocks:")
    for _, stock in quality_stocks.iterrows():
        current_weight = stock['portfolio_weight']
        if stock['red_flags'] <= 2:
            target_weight = min(20, current_weight * 1.5)
            print(f"   📈 {stock['Symbol']}: Increase from {current_weight:.1f}% to {target_weight:.1f}%")
        else:
            print(f"   ⚖️ {stock['Symbol']}: Quality stock but monitor risk factors")
else:
    print("   🔍 Need to research and add new high-quality stocks from outside portfolio")

print()

# Final portfolio health assessment
print("=" * 80)
print("PORTFOLIO HEALTH SCORECARD")
print("=" * 80)
print()

# Calculate composite score
risk_score = 100 - (df['red_flags'].mean() / 7 * 100)  # Lower red flags = higher score
quality_score = df['green_flags'].mean() / 11 * 100   # Higher green flags = higher score
balance_score = 100 - abs(50 - current_ideal - current_good)  # Closer to balanced = higher score

composite_score = (risk_score * 0.4 + quality_score * 0.4 + balance_score * 0.2)

print(f"📊 PORTFOLIO HEALTH METRICS:")
print(f"Risk Management Score: {risk_score:.1f}/100")
print(f"Quality Score: {quality_score:.1f}/100")
print(f"Balance Score: {balance_score:.1f}/100")
print(f"Composite Score: {composite_score:.1f}/100")
print()

if composite_score >= 80:
    overall_grade = "A"
    assessment = "Excellent portfolio with low risk and high quality"
elif composite_score >= 60:
    overall_grade = "B"
    assessment = "Good portfolio with room for improvement"
elif composite_score >= 40:
    overall_grade = "C"
    assessment = "Average portfolio needing significant improvement"
else:
    overall_grade = "D"
    assessment = "Poor portfolio requiring major restructuring"

print(f"Overall Portfolio Grade: {overall_grade}")
print(f"Assessment: {assessment}")
print()

# Strategic recommendations
print("🎯 STRATEGIC RECOMMENDATIONS:")
print()

print("1. IMMEDIATE ACTIONS (Next 2 weeks):")
if len(immediate_exits) > 0:
    print(f"   • Exit {len(immediate_exits)} stocks with high risk + low quality")
else:
    print("   • No immediate exits required, focus on position optimization")

print(f"   • Reduce high-risk exposure from {df[df['red_flags'] >= 5]['portfolio_weight'].sum():.1f}% to <5%")
print(f"   • Document lessons learned from risk analysis")
print()

print("2. MEDIUM-TERM GOALS (3-6 months):")
print(f"   • Increase high-quality allocation from {current_ideal:.1f}% to 40-50%")
print(f"   • Improve composite portfolio score from {composite_score:.1f} to 70+")
print(f"   • Achieve portfolio grade of B+ or higher")
print()

print("3. LONG-TERM VISION (12+ months):")
print("   • Build a portfolio dominated by low-risk, high-quality stocks")
print("   • Achieve systematic 15-20% annual returns with controlled risk")
print("   • Establish disciplined investment process based on objective criteria")
print()

print("💡 KEY SUCCESS FACTORS:")
print("   • Discipline in following matrix-based decisions")
print("   • Patience with quality stocks during market volatility")
print("   • Continuous monitoring and rebalancing")
print("   • Focus on business fundamentals over market sentiment")
print("   • Learning from both risk and quality analysis frameworks")
print()

# Export final summary
print("🔍 FINAL MATRIX SUMMARY:")
summary_matrix = df[['Symbol', 'red_flags', 'green_flags', 'matrix_classification', 'recommended_action', 'portfolio_weight', 'current_loss']].copy()
summary_matrix = summary_matrix.sort_values(['red_flags', 'green_flags'], ascending=[True, False])
print(summary_matrix.to_string(index=False, float_format='%.1f'))