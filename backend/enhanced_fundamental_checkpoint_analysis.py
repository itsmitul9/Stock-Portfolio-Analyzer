import pandas as pd
import numpy as np

print("=" * 80)
print("ENHANCED FUNDAMENTAL ANALYSIS")
print("RED FLAG CHECKPOINT FRAMEWORK")
print("=" * 80)
print()

# Define the checkpoint criteria (RED FLAGS)
checkpoint_criteria = {
    'roe_3y_avg': 'Average ROE 3Years < 10%',
    'debt_equity': 'Debt to Equity > 1.0',
    'promoter_holding': 'Promoter Holding < 20%',
    'pledged_percentage': 'Pledged Percentage > 30%',
    'debt_trend': 'Debt increasing (3Y back > 5Y back)',
    'return_3y': 'Stock Return 3Years < 10%',
    'return_1y': 'Stock Return 1Year < 10%'
}

print("🚨 RED FLAG CRITERIA FRAMEWORK:")
for i, (key, description) in enumerate(checkpoint_criteria.items(), 1):
    print(f"{i}. {description}")
print()

# Portfolio checkpoint analysis with estimated data
# Note: In real analysis, these would come from financial databases
checkpoint_data = {
    'Symbol': ['CDSL', 'CHENNPETRO', 'COCHINSHIP', 'ENGINERSIN', 'FACT', 'GSFC',
               'KALYANKJIL', 'MOIL', 'NETWEB', 'NOVAAGRI', 'PROTEAN', 'RITES', 'SCILAL'],

    # Financial Health Metrics
    'roe_3y_avg': [28.5, 9.2, 16.8, 13.5, 12.3, 7.8, 15.2, 8.9, 22.4, 4.2, 6.8, 14.7, 9.5],
    'debt_equity': [0.15, 0.42, 0.35, 0.25, 0.55, 1.25, 0.48, 0.22, 0.35, 1.45, 0.38, 0.28, 0.62],
    'promoter_holding': [24.8, 58.5, 36.2, 65.8, 69.2, 52.3, 61.4, 84.2, 42.5, 15.6, 28.4, 72.1, 18.5],
    'pledged_percentage': [0.0, 0.0, 12.5, 0.0, 0.0, 8.2, 22.4, 0.0, 18.7, 45.8, 38.5, 0.0, 42.1],
    'debt_3y_vs_5y': [0.8, 1.2, 1.4, 1.1, 1.3, 1.6, 1.5, 0.9, 1.8, 2.1, 1.7, 1.2, 1.4],  # Ratio: higher = debt increased
    'return_3y': [-12.5, -28.4, -45.2, -35.6, -18.7, -42.3, -25.8, -38.9, 15.2, -65.4, -72.1, -28.9, -58.7],
    'return_1y': [-17.6, -31.8, -30.5, -29.8, -24.5, -36.9, -36.9, -35.8, -6.0, -60.0, -67.4, -40.5, -55.2],

    # Current Portfolio Impact
    'current_loss_pct': [-17.59, -31.77, -30.54, -29.78, -24.52, -36.93, -36.87, -35.83, -6.00, -60.04, -67.39, -40.51, -55.22],
    'portfolio_weight': [13.6, 10.3, 2.8, 0.7, 26.9, 2.9, 2.7, 14.5, 11.1, 2.8, 0.7, 2.7, 8.5]
}

df = pd.DataFrame(checkpoint_data)

# Apply checkpoint criteria to identify red flags
def apply_checkpoint(row):
    red_flags = 0
    flag_details = []

    # 1. Average ROE 3Years < 10%
    if row['roe_3y_avg'] < 10:
        red_flags += 1
        flag_details.append(f"Low ROE: {row['roe_3y_avg']:.1f}%")

    # 2. Debt to equity > 1
    if row['debt_equity'] > 1.0:
        red_flags += 1
        flag_details.append(f"High D/E: {row['debt_equity']:.2f}")

    # 3. Promoter holding < 20%
    if row['promoter_holding'] < 20:
        red_flags += 1
        flag_details.append(f"Low Promoter: {row['promoter_holding']:.1f}%")

    # 4. Pledged percentage > 30%
    if row['pledged_percentage'] > 30:
        red_flags += 1
        flag_details.append(f"High Pledge: {row['pledged_percentage']:.1f}%")

    # 5. Debt increasing trend (3Y back > 5Y back)
    if row['debt_3y_vs_5y'] > 1.3:  # 30% increase threshold
        red_flags += 1
        flag_details.append(f"Rising Debt: {((row['debt_3y_vs_5y']-1)*100):.0f}% increase")

    # 6. Return over 3years < 10%
    if row['return_3y'] < 10:
        red_flags += 1
        flag_details.append(f"Poor 3Y Return: {row['return_3y']:.1f}%")

    # 7. Return over 1year < 10%
    if row['return_1y'] < 10:
        red_flags += 1
        flag_details.append(f"Poor 1Y Return: {row['return_1y']:.1f}%")

    return red_flags, flag_details

# Apply checkpoint analysis
checkpoint_results = df.apply(apply_checkpoint, axis=1)
df['red_flag_count'] = [result[0] for result in checkpoint_results]
df['red_flag_details'] = [result[1] for result in checkpoint_results]

# Risk categorization based on red flag count
def get_risk_category(red_flags):
    if red_flags >= 5:
        return 'EXTREMELY HIGH RISK'
    elif red_flags >= 4:
        return 'HIGH RISK'
    elif red_flags >= 3:
        return 'MEDIUM-HIGH RISK'
    elif red_flags >= 2:
        return 'MEDIUM RISK'
    elif red_flags >= 1:
        return 'LOW-MEDIUM RISK'
    else:
        return 'LOW RISK'

df['risk_category'] = df['red_flag_count'].apply(get_risk_category)

# Sort by red flag count (highest risk first)
df_sorted = df.sort_values(['red_flag_count', 'portfolio_weight'], ascending=[False, False])

print("📊 CHECKPOINT ANALYSIS RESULTS:")
print("=" * 80)
print()

print(f"{'Stock':<12} {'Flags':<6} {'Risk Category':<18} {'Weight%':<8} {'Current Loss%':<12}")
print("-" * 70)

for _, stock in df_sorted.iterrows():
    print(f"{stock['Symbol']:<12} {stock['red_flag_count']:<6} {stock['risk_category']:<18} {stock['portfolio_weight']:<8.1f} {stock['current_loss_pct']:<12.1f}")

print()
print("=" * 80)
print("DETAILED RED FLAG ANALYSIS")
print("=" * 80)
print()

# Group stocks by risk category
risk_groups = df_sorted.groupby('risk_category')

for risk_level, group in risk_groups:
    print(f"🚨 {risk_level}:")
    print(f"   Portfolio Weight: {group['portfolio_weight'].sum():.1f}%")
    print(f"   Average Loss: {group['current_loss_pct'].mean():.1f}%")
    print()

    for _, stock in group.iterrows():
        print(f"   📍 {stock['Symbol']} - {stock['red_flag_count']} Red Flags:")
        for detail in stock['red_flag_details']:
            print(f"      ❌ {detail}")
        print()

# Enhanced action plan based on checkpoint analysis
print("=" * 80)
print("CHECKPOINT-BASED ACTION PLAN")
print("=" * 80)
print()

extremely_high_risk = df_sorted[df_sorted['red_flag_count'] >= 5]
high_risk = df_sorted[df_sorted['red_flag_count'] == 4]
medium_high_risk = df_sorted[df_sorted['red_flag_count'] == 3]
medium_risk = df_sorted[df_sorted['red_flag_count'] == 2]
low_risk = df_sorted[df_sorted['red_flag_count'] <= 1]

print("🔴 IMMEDIATE EXIT (5+ Red Flags):")
if len(extremely_high_risk) > 0:
    total_weight = extremely_high_risk['portfolio_weight'].sum()
    for _, stock in extremely_high_risk.iterrows():
        print(f"   ❌ {stock['Symbol']}: {stock['red_flag_count']} red flags, {stock['portfolio_weight']:.1f}% weight")
        print(f"      Critical Issues: {', '.join(stock['red_flag_details'][:3])}")
    print(f"   Total Portfolio Impact: {total_weight:.1f}%")
else:
    print("   ✅ No stocks with 5+ red flags")
print()

print("🟠 HIGH PRIORITY EXIT (4 Red Flags):")
if len(high_risk) > 0:
    total_weight = high_risk['portfolio_weight'].sum()
    for _, stock in high_risk.iterrows():
        print(f"   ⚠️ {stock['Symbol']}: {stock['red_flag_count']} red flags, {stock['portfolio_weight']:.1f}% weight")
        print(f"      Major Issues: {', '.join(stock['red_flag_details'][:2])}")
    print(f"   Total Portfolio Impact: {total_weight:.1f}%")
else:
    print("   ✅ No stocks with exactly 4 red flags")
print()

print("🟡 REVIEW & REDUCE (3 Red Flags):")
if len(medium_high_risk) > 0:
    total_weight = medium_high_risk['portfolio_weight'].sum()
    for _, stock in medium_high_risk.iterrows():
        print(f"   📋 {stock['Symbol']}: {stock['red_flag_count']} red flags, {stock['portfolio_weight']:.1f}% weight")
        print(f"      Key Issues: {', '.join(stock['red_flag_details'][:2])}")
    print(f"   Action: Reduce position by 50-70%")
    print(f"   Total Portfolio Impact: {total_weight:.1f}%")
else:
    print("   ✅ No stocks with exactly 3 red flags")
print()

print("🟢 CONDITIONAL HOLD (≤2 Red Flags):")
safer_stocks = df_sorted[df_sorted['red_flag_count'] <= 2]
if len(safer_stocks) > 0:
    total_weight = safer_stocks['portfolio_weight'].sum()
    for _, stock in safer_stocks.iterrows():
        if stock['red_flag_count'] > 0:
            print(f"   ✓ {stock['Symbol']}: {stock['red_flag_count']} red flags, {stock['portfolio_weight']:.1f}% weight")
            if stock['red_flag_details']:
                print(f"      Minor Issues: {', '.join(stock['red_flag_details'][:1])}")
        else:
            print(f"   ✅ {stock['Symbol']}: No red flags, {stock['portfolio_weight']:.1f}% weight - QUALITY STOCK")
    print(f"   Total Portfolio Impact: {total_weight:.1f}%")
print()

# Portfolio health score
total_portfolio_weight = df['portfolio_weight'].sum()
high_risk_weight = df_sorted[df_sorted['red_flag_count'] >= 4]['portfolio_weight'].sum()
medium_risk_weight = df_sorted[df_sorted['red_flag_count'] == 3]['portfolio_weight'].sum()
low_risk_weight = df_sorted[df_sorted['red_flag_count'] <= 2]['portfolio_weight'].sum()

print("📊 PORTFOLIO HEALTH SCORECARD:")
print(f"High Risk Exposure (4+ flags): {high_risk_weight:.1f}%")
print(f"Medium Risk Exposure (3 flags): {medium_risk_weight:.1f}%")
print(f"Lower Risk Exposure (≤2 flags): {low_risk_weight:.1f}%")
print()

health_score = (low_risk_weight * 1 + medium_risk_weight * 0.5 + high_risk_weight * 0) / total_portfolio_weight * 100
print(f"Portfolio Health Score: {health_score:.1f}/100")

if health_score >= 80:
    grade = "A"
elif health_score >= 60:
    grade = "B"
elif health_score >= 40:
    grade = "C"
elif health_score >= 20:
    grade = "D"
else:
    grade = "F"

print(f"Portfolio Grade: {grade}")
print()

# Recovery timeline based on checkpoint analysis
print("=" * 80)
print("CHECKPOINT-BASED RECOVERY TIMELINE")
print("=" * 80)
print()

print("WEEK 1: Exit stocks with 5+ red flags")
week1_stocks = df_sorted[df_sorted['red_flag_count'] >= 5]['Symbol'].tolist()
print(f"Actions: {', '.join(week1_stocks) if week1_stocks else 'No immediate exits required'}")

print(f"\nWEEK 2-3: Exit/reduce stocks with 4+ red flags")
week2_stocks = df_sorted[df_sorted['red_flag_count'] == 4]['Symbol'].tolist()
print(f"Actions: {', '.join(week2_stocks) if week2_stocks else 'No high-priority exits'}")

print(f"\nMONTH 2: Review and reduce stocks with 3 red flags")
month2_stocks = df_sorted[df_sorted['red_flag_count'] == 3]['Symbol'].tolist()
print(f"Actions: {', '.join(month2_stocks) if month2_stocks else 'No medium-risk positions to reduce'}")

print(f"\nMONTH 3+: Focus capital on stocks with ≤2 red flags")
quality_stocks = df_sorted[df_sorted['red_flag_count'] <= 2]['Symbol'].tolist()
print(f"Quality Holdings: {', '.join(quality_stocks)}")

print()
print("🎯 KEY INSIGHT: Systematic elimination of red flag stocks")
print("   should significantly improve portfolio risk profile")
print(f"   Current high-risk exposure: {high_risk_weight:.1f}%")
print(f"   Target high-risk exposure: <5%")
print()

# Export summary for action
summary_df = df_sorted[['Symbol', 'red_flag_count', 'risk_category', 'portfolio_weight', 'current_loss_pct']].copy()
print("SUMMARY TABLE FOR ACTION:")
print(summary_df.to_string(index=False, float_format='%.1f'))