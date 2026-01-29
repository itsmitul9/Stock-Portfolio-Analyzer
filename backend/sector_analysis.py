import pandas as pd

# Sector classification for the portfolio stocks
sector_mapping = {
    'CDSL': 'Financial Services',
    'CHENNPETRO': 'Oil & Gas',
    'COCHINSHIP': 'Capital Goods',
    'ENGINERSIN': 'Capital Goods',
    'FACT': 'Chemicals',
    'GSFC': 'Chemicals',
    'KALYANKJIL': 'Consumer Discretionary',
    'MOIL': 'Metals & Mining',
    'NETWEB': 'Technology',
    'NOVAAGRI': 'Agriculture',
    'PROTEAN': 'Technology/Services',
    'RITES': 'Capital Goods',
    'SCILAL': 'Pharmaceuticals'
}

# Business analysis for each stock
business_analysis = {
    'CDSL': {
        'business': 'Central Depository Services - Monopolistic business',
        'concern': 'Regulatory changes, competition from NSDL',
        'recovery_potential': 'HIGH - Strong moat, growing demat accounts',
        'action': 'HOLD - Temporary correction'
    },
    'CHENNPETRO': {
        'business': 'Petroleum refinery under ONGC',
        'concern': 'Crude price volatility, margin pressure',
        'recovery_potential': 'MEDIUM - Depends on crude prices',
        'action': 'MONITOR - Oil price dependent'
    },
    'COCHINSHIP': {
        'business': 'Shipyard - Defense and commercial vessels',
        'concern': 'Execution delays, order book concerns',
        'recovery_potential': 'MEDIUM - Defense orders positive',
        'action': 'PARTIAL EXIT - High volatility sector'
    },
    'ENGINERSIN': {
        'business': 'Railways engineering consultancy',
        'concern': 'Project delays, competition',
        'recovery_potential': 'MEDIUM - Railway capex positive',
        'action': 'HOLD - Railway focus theme'
    },
    'FACT': {
        'business': 'Fertilizer company',
        'concern': 'Subsidy delays, raw material costs',
        'recovery_potential': 'LOW-MEDIUM - Cyclical business',
        'action': 'REDUCE POSITION - Too large (27%)'
    },
    'GSFC': {
        'business': 'Gujarat State Fertilizer Company',
        'concern': 'Same as FACT + state PSU issues',
        'recovery_potential': 'LOW - Multiple headwinds',
        'action': 'EXIT - Poor fundamentals'
    },
    'KALYANKJIL': {
        'business': 'Jewelry retailer',
        'concern': 'Gold price volatility, competition',
        'recovery_potential': 'MEDIUM - Wedding season demand',
        'action': 'PARTIAL EXIT - Reduce exposure'
    },
    'MOIL': {
        'business': 'Manganese ore mining',
        'concern': 'Commodity cycle, export restrictions',
        'recovery_potential': 'LOW - Cyclical downturn',
        'action': 'EXIT - Commodity in downcycle'
    },
    'NETWEB': {
        'business': 'Data center and cloud services',
        'concern': 'High valuation, competition',
        'recovery_potential': 'HIGH - AI/Cloud growth theme',
        'action': 'HOLD - Only small loss, growth sector'
    },
    'NOVAAGRI': {
        'business': 'Agricultural products trading',
        'concern': 'Weather dependency, margin pressure',
        'recovery_potential': 'VERY LOW - Struggling business',
        'action': 'IMMEDIATE EXIT - Fundamental issues'
    },
    'PROTEAN': {
        'business': 'eGovernance services',
        'concern': 'Execution issues, competitive pressure',
        'recovery_potential': 'VERY LOW - Business model issues',
        'action': 'IMMEDIATE EXIT - Cut losses'
    },
    'RITES': {
        'business': 'Railway consultancy and export',
        'concern': 'Project execution, international exposure',
        'recovery_potential': 'MEDIUM - Railway capex theme',
        'action': 'HOLD - Monitor quarterly results'
    },
    'SCILAL': {
        'business': 'Pharmaceutical company',
        'concern': 'US FDA issues, pricing pressure',
        'recovery_potential': 'LOW - Regulatory overhang',
        'action': 'EXIT - Regulatory issues persist'
    }
}

print("=" * 80)
print("SECTOR-WISE ANALYSIS & RECOVERY STRATEGY")
print("=" * 80)
print()

# Calculate sector exposure
portfolio_data = {
    'Symbol': ['CDSL', 'CHENNPETRO', 'COCHINSHIP', 'ENGINERSIN', 'FACT', 'GSFC',
               'KALYANKJIL', 'MOIL', 'NETWEB', 'NOVAAGRI', 'PROTEAN', 'RITES', 'SCILAL'],
    'Investment_Value': [497947, 377513.76, 102580, 24849, 986957.4, 105600, 98884.8, 530500, 407370.6, 101812.04, 23980, 100584, 311100],
    'Current_Value': [410351.1, 257571.6, 71249.4, 17449.2, 745001.4, 66604.8, 62426.7, 340400, 382941, 40684.82, 7819.9, 59835.6, 139320],
    'Loss_Pct': [-17.59, -31.77, -30.54, -29.78, -24.52, -36.93, -36.87, -35.83, -6.00, -60.04, -67.39, -40.51, -55.22]
}

df = pd.DataFrame(portfolio_data)
df['Sector'] = df['Symbol'].map(sector_mapping)
df['Loss_Amount'] = df['Investment_Value'] - df['Current_Value']

# Sector-wise aggregation
sector_analysis = df.groupby('Sector').agg({
    'Investment_Value': 'sum',
    'Current_Value': 'sum',
    'Loss_Amount': 'sum',
    'Symbol': 'count'
}).reset_index()
sector_analysis.columns = ['Sector', 'Investment', 'Current_Value', 'Loss_Amount', 'Stocks_Count']
sector_analysis['Loss_Pct'] = (sector_analysis['Loss_Amount'] / sector_analysis['Investment']) * 100
sector_analysis['Portfolio_Weight'] = (sector_analysis['Investment'] / sector_analysis['Investment'].sum()) * 100

print("SECTOR EXPOSURE & PERFORMANCE:")
print(sector_analysis[['Sector', 'Stocks_Count', 'Portfolio_Weight', 'Loss_Pct', 'Loss_Amount']].to_string(index=False, float_format='%.2f'))
print()

# Identify problematic sectors
print("SECTOR-WISE CONCERNS:")
print()

# Group by sectors and analyze
worst_sectors = sector_analysis.nlargest(3, 'Loss_Pct')
for _, sector in worst_sectors.iterrows():
    print(f"🔴 {sector['Sector']} - Loss: {sector['Loss_Pct']:.1f}% (₹{sector['Loss_Amount']:,.0f})")
    sector_stocks = df[df['Sector'] == sector['Sector']]
    for _, stock in sector_stocks.iterrows():
        analysis = business_analysis[stock['Symbol']]
        print(f"   {stock['Symbol']}: {analysis['concern']}")
        print(f"   Recovery Potential: {analysis['recovery_potential']}")
        print(f"   Action: {analysis['action']}")
    print()

print("=" * 80)
print("COMPREHENSIVE RECOVERY PLAN")
print("=" * 80)
print()

# Phase-wise exit plan
print("PHASE 1 - IMMEDIATE EXITS (This Week):")
immediate_exits = ['PROTEAN', 'NOVAAGRI', 'SCILAL']
immediate_exit_data = df[df['Symbol'].isin(immediate_exits)]
total_immediate_loss = immediate_exit_data['Loss_Amount'].sum()
total_immediate_recovery = immediate_exit_data['Current_Value'].sum()

print(f"Exit {len(immediate_exits)} stocks with combined loss of ₹{total_immediate_loss:,.0f}")
print(f"Recover ₹{total_immediate_recovery:,.0f} in cash")
for stock in immediate_exits:
    analysis = business_analysis[stock]
    print(f"• {stock}: {analysis['action']} - {analysis['recovery_potential']}")
print()

print("PHASE 2 - PARTIAL EXITS (Next Month):")
partial_exits = ['GSFC', 'MOIL', 'FACT']  # FACT to reduce position size
print("Reduce exposure by 50-70% in these positions:")
for stock in partial_exits:
    analysis = business_analysis[stock]
    stock_data = df[df['Symbol'] == stock].iloc[0]
    if stock == 'FACT':
        print(f"• {stock}: Reduce from 27% to 10% portfolio weight - Overconcentration risk")
    else:
        print(f"• {stock}: Exit 70% - {analysis['concern']}")
print()

print("PHASE 3 - MONITOR & DECIDE (3-6 months):")
monitor_stocks = ['RITES', 'KALYANKJIL', 'COCHINSHIP', 'CHENNPETRO', 'ENGINERSIN']
print("Set stop-loss at additional 15% decline:")
for stock in monitor_stocks:
    analysis = business_analysis[stock]
    print(f"• {stock}: {analysis['recovery_potential']} - Monitor quarterly results")
print()

print("PHASE 4 - HOLD & BUILD (Long-term):")
hold_stocks = ['CDSL', 'NETWEB']
print("Strong fundamental businesses with temporary corrections:")
for stock in hold_stocks:
    analysis = business_analysis[stock]
    print(f"• {stock}: {analysis['recovery_potential']} - {analysis['business']}")
print()

# Calculate recovery scenarios
total_investment = df['Investment_Value'].sum()
total_current = df['Current_Value'].sum()

print("=" * 80)
print("FINANCIAL RECOVERY SCENARIOS")
print("=" * 80)
print()

# Scenario 1: Follow the plan
phase1_recovery = immediate_exit_data['Current_Value'].sum()
remaining_after_phase1 = total_current - phase1_recovery

print("SCENARIO 1 - Follow Phased Exit Plan:")
print(f"Phase 1 cash recovery: ₹{phase1_recovery:,.0f}")
print(f"Remaining portfolio value: ₹{remaining_after_phase1:,.0f}")
print(f"If remaining portfolio recovers 30% over 12 months:")
print(f"Total portfolio value: ₹{phase1_recovery + (remaining_after_phase1 * 1.3):,.0f}")
print(f"Recovery from current: {((phase1_recovery + (remaining_after_phase1 * 1.3) - total_current)/total_current)*100:.1f}%")
print()

# Tax loss harvesting calculation
ltcg_losses = df[df['Symbol'].isin(['PROTEAN', 'NOVAAGRI', 'SCILAL', 'GSFC', 'MOIL'])]['Loss_Amount'].sum()
print("TAX LOSS HARVESTING BENEFIT:")
print(f"LTCG losses available for offset: ₹{ltcg_losses:,.0f}")
print(f"Tax savings on future LTCG (10%): ₹{ltcg_losses * 0.10:,.0f}")
print()

print("=" * 80)
print("ACTION CHECKLIST")
print("=" * 80)
print()

print("✅ WEEK 1 ACTIONS:")
print("1. Place sell orders for PROTEAN, NOVAAGRI, SCILAL")
print("2. Book LTCG losses of ₹{:,.0f}".format(immediate_exit_data['Loss_Amount'].sum()))
print("3. Review and document lessons learned")
print()

print("✅ WEEK 2-4 ACTIONS:")
print("1. Reduce FACT position from 27% to 10% of portfolio")
print("2. Exit 70% positions in GSFC and MOIL")
print("3. Research better investment opportunities")
print()

print("✅ ONGOING MONITORING:")
print("1. Set 15% additional stop-loss on remaining positions")
print("2. Review quarterly results for monitor-category stocks")
print("3. Maintain maximum 10% position size per stock")
print("4. Focus on quality businesses with strong moats")
print()

print("⚠️  RISK MANAGEMENT RULES:")
print("• Never average down on stocks already showing 30%+ losses")
print("• Exit any position that falls additional 15% from current levels")
print("• Maintain diversification across sectors")
print("• Don't invest in cyclical commodities during downcycle")
print()

# Expected timeline for recovery
print("RECOVERY TIMELINE EXPECTATIONS:")
print("• 6 months: Portfolio stabilization after exits")
print("• 12 months: 20-30% recovery from current levels")
print("• 24 months: Potential to recover 70-80% of losses with disciplined approach")
print("• Key: Focus on quality, avoid speculation, maintain discipline")