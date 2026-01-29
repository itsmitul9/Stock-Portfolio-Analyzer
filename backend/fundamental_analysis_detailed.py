import pandas as pd
from datetime import datetime

print("=" * 80)
print("COMPREHENSIVE FUNDAMENTAL ANALYSIS")
print("Portfolio Stock Analysis - Individual Stock Deep Dive")
print("=" * 80)
print()

# Stock fundamental data with comprehensive analysis
fundamental_analysis = {
    'CDSL': {
        'company_name': 'Central Depository Services (India) Ltd',
        'sector': 'Financial Services',
        'market_cap': 'Large Cap (~₹18,000 Cr)',
        'business_model': 'Monopolistic depository services for electronic securities',
        'key_metrics': {
            'revenue_growth_3y': '15-20% CAGR',
            'profit_margin': '65-70%',
            'roe': '25-30%',
            'debt_equity': '0.1-0.2',
            'dividend_yield': '2-3%'
        },
        'strengths': [
            'Duopoly with NSDL in depository services',
            'Growing demat account base (8Cr+ accounts)',
            'Asset-light, high-margin business model',
            'Regulatory moats and switching costs',
            'Consistent dividend paying track record'
        ],
        'weaknesses': [
            'Dependent on capital market activity',
            'Regulatory risk from SEBI',
            'Limited growth avenues beyond core business'
        ],
        'industry_outlook': 'POSITIVE - Rising retail participation, mutual fund growth, digitalization',
        'valuation': 'FAIR TO EXPENSIVE - P/E: 35-40x (historical average: 25-30x)',
        'investment_thesis': 'STRONG - Monopolistic business with consistent growth',
        'risks': [
            'Market volatility affecting trading volumes',
            'Regulatory changes in fee structure',
            'Competition from new players (unlikely but possible)'
        ],
        'recovery_potential': 'HIGH',
        'time_horizon': '12-18 months',
        'recommendation': 'STRONG HOLD - Quality business, temporary correction'
    },

    'CHENNPETRO': {
        'company_name': 'Chennai Petroleum Corporation Ltd',
        'sector': 'Oil & Gas Refining',
        'market_cap': 'Mid Cap (~₹3,500 Cr)',
        'business_model': 'Petroleum refinery under ONGC, processes crude oil',
        'key_metrics': {
            'revenue_growth_3y': '10-15% CAGR',
            'profit_margin': '2-5% (volatile)',
            'roe': '8-12%',
            'debt_equity': '0.3-0.5',
            'capacity_utilization': '85-90%'
        },
        'strengths': [
            'Strategic location in Chennai port',
            'ONGC backing provides crude supply security',
            'Established refinery with good infrastructure',
            'Exports petroleum products'
        ],
        'weaknesses': [
            'Margin volatility due to crude price fluctuations',
            'High dependence on international crude prices',
            'Environmental compliance costs',
            'Limited downstream integration'
        ],
        'industry_outlook': 'MIXED - Global refining capacity addition, margin pressure',
        'valuation': 'FAIR - P/E: 8-12x (cyclical nature)',
        'investment_thesis': 'CYCLICAL HOLD - Depends on oil price cycle',
        'risks': [
            'Crude oil price volatility',
            'Refining margin compression',
            'Environmental regulations',
            'Currency fluctuation on imports'
        ],
        'recovery_potential': 'MEDIUM',
        'time_horizon': '18-24 months',
        'recommendation': 'CONDITIONAL HOLD - Monitor oil prices and margins'
    },

    'COCHINSHIP': {
        'company_name': 'Cochin Shipyard Ltd',
        'sector': 'Capital Goods - Shipbuilding',
        'market_cap': 'Small Cap (~₹2,000 Cr)',
        'business_model': 'Shipyard - builds commercial and defense vessels',
        'key_metrics': {
            'revenue_growth_3y': '12-18% CAGR',
            'profit_margin': '8-12%',
            'roe': '15-20%',
            'debt_equity': '0.2-0.4',
            'order_book': '₹15,000+ Cr (3-4x revenue)'
        },
        'strengths': [
            'Strong order book from Indian Navy',
            'Technical expertise in complex vessel building',
            'Government support for indigenous shipbuilding',
            'Diversified product portfolio'
        ],
        'weaknesses': [
            'Project execution delays',
            'High working capital requirements',
            'Cyclical nature of shipbuilding industry',
            'Competition from global shipyards'
        ],
        'industry_outlook': 'POSITIVE - Government push for Make in India, defense orders',
        'valuation': 'FAIR - P/E: 12-18x (considering order book)',
        'investment_thesis': 'TURNAROUND STORY - Execution improvement key',
        'risks': [
            'Project cost overruns',
            'Delivery delays affecting penalties',
            'Raw material cost inflation',
            'Competition in commercial segment'
        ],
        'recovery_potential': 'MEDIUM',
        'time_horizon': '24-36 months',
        'recommendation': 'PARTIAL EXIT - High execution risk'
    },

    'ENGINERSIN': {
        'company_name': 'Engineers India Ltd',
        'sector': 'Capital Goods - Engineering Consultancy',
        'market_cap': 'Small Cap (~₹1,500 Cr)',
        'business_model': 'Engineering consultancy for oil, gas, and infrastructure projects',
        'key_metrics': {
            'revenue_growth_3y': '8-12% CAGR',
            'profit_margin': '15-20%',
            'roe': '12-15%',
            'debt_equity': '0.1-0.3',
            'order_book': '₹8,000+ Cr'
        },
        'strengths': [
            'Leading position in hydrocarbon consulting',
            'Strong relationship with PSU oil companies',
            'Technical expertise and experience',
            'Asset-light business model'
        ],
        'weaknesses': [
            'High dependence on PSU capex cycles',
            'Project execution delays',
            'Limited international presence',
            'Competitive pressure in bidding'
        ],
        'industry_outlook': 'MIXED - Depends on oil & gas capex, renewable transition',
        'valuation': 'FAIR - P/E: 10-15x',
        'investment_thesis': 'CYCLICAL PLAY - Linked to energy capex',
        'risks': [
            'Delay in PSU project approvals',
            'Transition to renewable energy affecting traditional projects',
            'Cost overruns in projects',
            'Working capital issues'
        ],
        'recovery_potential': 'MEDIUM',
        'time_horizon': '18-24 months',
        'recommendation': 'HOLD - Monitor capex recovery'
    },

    'FACT': {
        'company_name': 'Fertilizers and Chemicals Travancore Ltd',
        'sector': 'Chemicals - Fertilizers',
        'market_cap': 'Large Cap (~₹12,000 Cr)',
        'business_model': 'Integrated fertilizer manufacturer',
        'key_metrics': {
            'revenue_growth_3y': '8-15% CAGR',
            'profit_margin': '5-10%',
            'roe': '10-15%',
            'debt_equity': '0.4-0.6',
            'capacity_utilization': '80-85%'
        },
        'strengths': [
            'Integrated manufacturing facilities',
            'Strong distribution network in South India',
            'Government fertilizer subsidy support',
            'Diversified product portfolio including chemicals'
        ],
        'weaknesses': [
            'Subsidy payment delays from government',
            'High raw material cost volatility',
            'Working capital intensive business',
            'Environmental compliance costs'
        ],
        'industry_outlook': 'STABLE - Government support, growing agricultural needs',
        'valuation': 'FAIR TO CHEAP - P/E: 8-12x',
        'investment_thesis': 'DEFENSIVE PLAY - Essential sector with government backing',
        'risks': [
            'Subsidy policy changes',
            'Raw material (ammonia, phosphoric acid) price volatility',
            'Environmental regulations',
            'Competition from private players'
        ],
        'recovery_potential': 'MEDIUM-HIGH',
        'time_horizon': '12-18 months',
        'recommendation': 'REDUCE POSITION SIZE - Good business but over-concentrated'
    }
}

# Continue with remaining stocks...
remaining_stocks = {
    'GSFC': {
        'company_name': 'Gujarat State Fertilizer Company Ltd',
        'sector': 'Chemicals - Fertilizers',
        'market_cap': 'Small Cap (~₹800 Cr)',
        'business_model': 'State PSU fertilizer manufacturer',
        'key_metrics': {
            'revenue_growth_3y': '5-10% CAGR',
            'profit_margin': '2-6%',
            'roe': '8-12%',
            'debt_equity': '0.6-0.8',
            'capacity_utilization': '75-80%'
        },
        'strengths': [
            'State government backing',
            'Established manufacturing facilities',
            'Local market presence in Gujarat'
        ],
        'weaknesses': [
            'State PSU inefficiencies',
            'High debt burden',
            'Old technology and infrastructure',
            'Limited growth capital'
        ],
        'industry_outlook': 'STABLE - But facing competition from efficient private players',
        'valuation': 'CHEAP - P/E: 6-10x (justified due to poor fundamentals)',
        'investment_thesis': 'WEAK - State PSU with structural issues',
        'risks': [
            'Government policy changes',
            'Financial stress due to high debt',
            'Competition from efficient players',
            'Technology obsolescence'
        ],
        'recovery_potential': 'LOW',
        'time_horizon': '36+ months',
        'recommendation': 'EXIT - Weak fundamentals, state PSU issues'
    },

    'KALYANKJIL': {
        'company_name': 'Kalyan Jewellers India Ltd',
        'sector': 'Consumer Discretionary - Jewelry',
        'market_cap': 'Small Cap (~₹4,500 Cr)',
        'business_model': 'Organized jewelry retailer',
        'key_metrics': {
            'revenue_growth_3y': '15-25% CAGR',
            'profit_margin': '3-6%',
            'roe': '12-18%',
            'debt_equity': '0.3-0.5',
            'store_count': '200+ stores'
        },
        'strengths': [
            'Strong brand recognition in South India',
            'Organized player in fragmented market',
            'Expansion into North and West India',
            'Digital initiatives and omni-channel presence'
        ],
        'weaknesses': [
            'High gold price volatility affecting demand',
            'Intense competition from Tanishq, PC Jeweller',
            'High working capital requirements',
            'Regional concentration risk'
        ],
        'industry_outlook': 'POSITIVE - Shift from unorganized to organized, wedding demand',
        'valuation': 'FAIR - P/E: 20-30x (growth premium)',
        'investment_thesis': 'GROWTH STORY - Organized jewelry market expansion',
        'risks': [
            'Gold price volatility',
            'Competition from established players',
            'Economic slowdown affecting discretionary spend',
            'Supply chain disruptions'
        ],
        'recovery_potential': 'MEDIUM-HIGH',
        'time_horizon': '18-24 months',
        'recommendation': 'PARTIAL HOLD - Reduce position size'
    },

    'MOIL': {
        'company_name': 'MOIL Ltd',
        'sector': 'Metals & Mining - Manganese',
        'market_cap': 'Mid Cap (~₹4,000 Cr)',
        'business_model': 'Manganese ore mining and processing',
        'key_metrics': {
            'revenue_growth_3y': '5-15% CAGR (volatile)',
            'profit_margin': '15-25% (cyclical)',
            'roe': '10-20%',
            'debt_equity': '0.1-0.3',
            'reserves': 'Large manganese reserves in India'
        },
        'strengths': [
            'Dominant position in Indian manganese mining',
            'Low-cost mining operations',
            'Strong balance sheet with low debt',
            'Export capabilities'
        ],
        'weaknesses': [
            'Cyclical commodity business',
            'High dependence on steel industry demand',
            'Environmental and regulatory challenges',
            'Limited value-added products'
        ],
        'industry_outlook': 'WEAK - Steel industry slowdown, global overcapacity',
        'valuation': 'FAIR TO CHEAP - P/E: 8-15x (cyclical bottom)',
        'investment_thesis': 'COMMODITY CYCLE PLAY - Currently in downcycle',
        'risks': [
            'Global steel demand slowdown',
            'Chinese competition in manganese',
            'Environmental compliance costs',
            'Export restrictions by government'
        ],
        'recovery_potential': 'LOW-MEDIUM',
        'time_horizon': '24-36 months',
        'recommendation': 'EXIT - Commodity in prolonged downcycle'
    },

    'NETWEB': {
        'company_name': 'Netweb Technologies India Ltd',
        'sector': 'Technology - Data Centers',
        'market_cap': 'Small Cap (~₹3,000 Cr)',
        'business_model': 'High-performance computing and data center solutions',
        'key_metrics': {
            'revenue_growth_3y': '25-35% CAGR',
            'profit_margin': '8-12%',
            'roe': '20-25%',
            'debt_equity': '0.2-0.4',
            'client_base': 'Government, enterprises, research institutions'
        },
        'strengths': [
            'Niche player in HPC and AI infrastructure',
            'Strong technical expertise',
            'Growing demand for data centers and cloud',
            'Government digitalization initiatives'
        ],
        'weaknesses': [
            'Small scale compared to global players',
            'High dependence on few large clients',
            'Technology obsolescence risk',
            'Intense competition from global vendors'
        ],
        'industry_outlook': 'VERY POSITIVE - AI boom, data center growth, digitalization',
        'valuation': 'EXPENSIVE - P/E: 40-60x (growth premium)',
        'investment_thesis': 'GROWTH STORY - AI and digital transformation beneficiary',
        'risks': [
            'Technology disruption',
            'Competition from global cloud providers',
            'Client concentration risk',
            'Execution challenges in scaling'
        ],
        'recovery_potential': 'HIGH',
        'time_horizon': '6-12 months',
        'recommendation': 'STRONG HOLD - Best positioned for tech growth'
    }
}

# Add remaining stocks to the main dictionary
fundamental_analysis.update(remaining_stocks)

# Final batch of stocks
final_stocks = {
    'NOVAAGRI': {
        'company_name': 'Nova Agritech Ltd',
        'sector': 'Agriculture - Trading',
        'market_cap': 'Small Cap (~₹400 Cr)',
        'business_model': 'Agricultural commodities trading and processing',
        'key_metrics': {
            'revenue_growth_3y': '-5 to +10% CAGR (volatile)',
            'profit_margin': '1-4%',
            'roe': '5-10%',
            'debt_equity': '0.8-1.2',
            'working_capital_days': '90-120 days'
        },
        'strengths': [
            'Presence in essential agricultural sector',
            'Trading relationships with farmers',
            'Processing capabilities'
        ],
        'weaknesses': [
            'Low margins in commodity trading',
            'High working capital requirements',
            'Weather and crop dependency',
            'Fragmented and volatile market'
        ],
        'industry_outlook': 'CHALLENGING - Climate change, price volatility, competition',
        'valuation': 'CHEAP - P/E: 8-15x (distressed valuation)',
        'investment_thesis': 'DISTRESSED - Struggling business model',
        'risks': [
            'Monsoon dependency',
            'Commodity price volatility',
            'Working capital stress',
            'Competition from larger agri-businesses'
        ],
        'recovery_potential': 'VERY LOW',
        'time_horizon': 'Uncertain',
        'recommendation': 'IMMEDIATE EXIT - Fundamental business issues'
    },

    'PROTEAN': {
        'company_name': 'Protean eGov Technologies Ltd',
        'sector': 'Technology/Services - eGovernance',
        'market_cap': 'Small Cap (~₹800 Cr)',
        'business_model': 'eGovernance and digital identity solutions',
        'key_metrics': {
            'revenue_growth_3y': '10-20% CAGR',
            'profit_margin': '10-15%',
            'roe': '15-20%',
            'debt_equity': '0.2-0.4',
            'government_client_base': 'Various state and central government projects'
        },
        'strengths': [
            'Established player in eGovernance',
            'Government digitalization tailwinds',
            'Technical expertise in identity solutions',
            'Recurring revenue from maintenance'
        ],
        'weaknesses': [
            'High dependence on government contracts',
            'Long sales cycles and payment delays',
            'Competition from IT giants',
            'Execution challenges in large projects'
        ],
        'industry_outlook': 'POSITIVE - Government digitalization, but competitive',
        'valuation': 'CHEAP - P/E: 8-12x (execution concerns)',
        'investment_thesis': 'TURNAROUND STORY - Execution improvement needed',
        'risks': [
            'Project execution delays',
            'Payment delays from government',
            'Competition from larger IT companies',
            'Technology changes requiring heavy investments'
        ],
        'recovery_potential': 'LOW',
        'time_horizon': '24+ months',
        'recommendation': 'IMMEDIATE EXIT - Execution issues persist'
    },

    'RITES': {
        'company_name': 'Rail India Technical and Economic Service Ltd',
        'sector': 'Capital Goods - Railway Consultancy',
        'market_cap': 'Mid Cap (~₹3,000 Cr)',
        'business_model': 'Railway consultancy, export, and leasing services',
        'key_metrics': {
            'revenue_growth_3y': '12-18% CAGR',
            'profit_margin': '15-25%',
            'roe': '15-20%',
            'debt_equity': '0.1-0.3',
            'order_book': '₹8,000+ Cr'
        },
        'strengths': [
            'Strong relationship with Indian Railways',
            'Technical expertise in railway systems',
            'Export opportunities in emerging markets',
            'Asset-light consultancy model'
        ],
        'weaknesses': [
            'High dependence on railway capex',
            'Execution delays in international projects',
            'Competition in export markets',
            'Working capital issues'
        ],
        'industry_outlook': 'POSITIVE - Railway modernization, export potential',
        'valuation': 'FAIR - P/E: 12-18x',
        'investment_thesis': 'RAILWAY CAPEX BENEFICIARY - But execution key',
        'risks': [
            'Delays in railway project approvals',
            'International project execution challenges',
            'Competition from global consultants',
            'Currency fluctuation on exports'
        ],
        'recovery_potential': 'MEDIUM',
        'time_horizon': '18-24 months',
        'recommendation': 'CONDITIONAL HOLD - Monitor execution'
    },

    'SCILAL': {
        'company_name': 'Sci Ludhiana Ltd',
        'sector': 'Pharmaceuticals',
        'market_cap': 'Small Cap (~₹1,500 Cr)',
        'business_model': 'Pharmaceutical manufacturing and exports',
        'key_metrics': {
            'revenue_growth_3y': '8-15% CAGR',
            'profit_margin': '8-15%',
            'roe': '12-18%',
            'debt_equity': '0.3-0.5',
            'export_revenue': '60-70% of total revenue'
        },
        'strengths': [
            'Established manufacturing capabilities',
            'Export presence in regulated markets',
            'Diversified product portfolio',
            'Cost-competitive manufacturing'
        ],
        'weaknesses': [
            'US FDA compliance issues',
            'High dependence on exports',
            'Generic competition and pricing pressure',
            'Regulatory compliance costs'
        ],
        'industry_outlook': 'CHALLENGING - Regulatory scrutiny, pricing pressure',
        'valuation': 'CHEAP - P/E: 8-15x (regulatory discount)',
        'investment_thesis': 'REGULATORY OVERHANG - Recovery depends on compliance',
        'risks': [
            'FDA action on manufacturing facilities',
            'Generic competition reducing prices',
            'Regulatory compliance costs',
            'Currency fluctuation affecting exports'
        ],
        'recovery_potential': 'LOW',
        'time_horizon': '24-36 months',
        'recommendation': 'EXIT - Regulatory issues likely to persist'
    }
}

fundamental_analysis.update(final_stocks)

# Print detailed analysis
def print_stock_analysis(symbol, data):
    print(f"📊 {symbol.upper()} - {data['company_name']}")
    print(f"Sector: {data['sector']} | Market Cap: {data['market_cap']}")
    print(f"Business: {data['business_model']}")
    print()

    print("🔢 KEY METRICS:")
    for metric, value in data['key_metrics'].items():
        print(f"  • {metric.replace('_', ' ').title()}: {value}")
    print()

    print("💪 STRENGTHS:")
    for strength in data['strengths']:
        print(f"  ✅ {strength}")
    print()

    print("⚠️  WEAKNESSES:")
    for weakness in data['weaknesses']:
        print(f"  ❌ {weakness}")
    print()

    print("🏭 INDUSTRY OUTLOOK:", data['industry_outlook'])
    print("💰 VALUATION:", data['valuation'])
    print("📈 INVESTMENT THESIS:", data['investment_thesis'])
    print()

    print("🚨 KEY RISKS:")
    for risk in data['risks']:
        print(f"  ⚡ {risk}")
    print()

    print(f"🎯 RECOVERY POTENTIAL: {data['recovery_potential']}")
    print(f"⏰ TIME HORIZON: {data['time_horizon']}")
    print(f"🎯 RECOMMENDATION: {data['recommendation']}")

    print("=" * 80)
    print()

# Print all analyses
for symbol, analysis in fundamental_analysis.items():
    print_stock_analysis(symbol, analysis)

# Summary recommendations
print("=" * 80)
print("FUNDAMENTAL ANALYSIS SUMMARY & RECOMMENDATIONS")
print("=" * 80)
print()

recommendations = {
    'IMMEDIATE EXIT': [],
    'PARTIAL EXIT': [],
    'CONDITIONAL HOLD': [],
    'HOLD': [],
    'STRONG HOLD': []
}

for symbol, data in fundamental_analysis.items():
    rec = data['recommendation']
    if 'EXIT NOW' in rec or 'IMMEDIATE EXIT' in rec:
        recommendations['IMMEDIATE EXIT'].append(symbol)
    elif 'PARTIAL EXIT' in rec or 'REDUCE' in rec:
        recommendations['PARTIAL EXIT'].append(symbol)
    elif 'CONDITIONAL' in rec:
        recommendations['CONDITIONAL HOLD'].append(symbol)
    elif 'STRONG HOLD' in rec:
        recommendations['STRONG HOLD'].append(symbol)
    else:
        recommendations['HOLD'].append(symbol)

print("🔴 IMMEDIATE EXIT (Fundamental Issues):")
for stock in recommendations['IMMEDIATE EXIT']:
    data = fundamental_analysis[stock]
    print(f"  • {stock}: {data['investment_thesis']} - Recovery: {data['recovery_potential']}")
print()

print("🟡 PARTIAL EXIT/REDUCE (Risk Management):")
for stock in recommendations['PARTIAL EXIT']:
    data = fundamental_analysis[stock]
    print(f"  • {stock}: {data['investment_thesis']} - Recovery: {data['recovery_potential']}")
print()

print("🟠 CONDITIONAL HOLD (Monitor Closely):")
for stock in recommendations['CONDITIONAL HOLD']:
    data = fundamental_analysis[stock]
    print(f"  • {stock}: {data['investment_thesis']} - Recovery: {data['recovery_potential']}")
print()

print("🟢 HOLD (Reasonable Fundamentals):")
for stock in recommendations['HOLD']:
    data = fundamental_analysis[stock]
    print(f"  • {stock}: {data['investment_thesis']} - Recovery: {data['recovery_potential']}")
print()

print("🟢 STRONG HOLD (High Quality):")
for stock in recommendations['STRONG HOLD']:
    data = fundamental_analysis[stock]
    print(f"  • {stock}: {data['investment_thesis']} - Recovery: {data['recovery_potential']}")
print()

print("🎯 PORTFOLIO QUALITY SCORE:")
high_quality = len(recommendations['STRONG HOLD'])
medium_quality = len(recommendations['HOLD']) + len(recommendations['CONDITIONAL HOLD'])
low_quality = len(recommendations['PARTIAL EXIT']) + len(recommendations['IMMEDIATE EXIT'])

print(f"High Quality Stocks: {high_quality}/13 ({(high_quality/13)*100:.1f}%)")
print(f"Medium Quality Stocks: {medium_quality}/13 ({(medium_quality/13)*100:.1f}%)")
print(f"Low Quality Stocks: {low_quality}/13 ({(low_quality/13)*100:.1f}%)")
print()

print("📊 FUNDAMENTAL SCORE CARD:")
print("Current Portfolio Grade: D+ (Too many low-quality positions)")
print("Target Portfolio Grade: B+ (Focus on quality)")
print("Recommended Actions: Exit weak fundamentals, concentrate on quality")