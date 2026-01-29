import pandas as pd
import csv

print("=" * 80)
print("COMPREHENSIVE STOCK ANALYSIS DATA EXPORT")
print("CSV File Generation with All Valuation Parameters")
print("=" * 80)
print()

# Define all the parameters and their explanations
parameter_explanations = {
    # Basic Information
    'Symbol': 'Stock ticker symbol',
    'Company_Name': 'Full company name',
    'Sector': 'Industry sector classification',
    'Market_Cap': 'Market capitalization in Crores',
    'Portfolio_Weight': 'Current allocation in portfolio (%)',
    'Current_Loss_Pct': 'Current loss percentage from purchase price',

    # Valuation Metrics (Quality Criteria)
    'Current_PE': 'Current Price to Earnings ratio',
    'Historical_PE_5Y': 'Average PE ratio over last 5 years',
    'Historical_PE_3Y': 'Average PE ratio over last 3 years',
    'PEG_Ratio': 'Price/Earnings to Growth ratio',
    'EPS_Growth_3Y': 'Earnings per share growth over 3 years (%)',
    'EPS_Growth_5Y': 'Earnings per share growth over 5 years (%)',

    # Performance Metrics
    'Return_1Y': 'Stock return over 1 year (%)',
    'Return_3Y': 'Stock return over 3 years (%)',
    'ROE_Current': 'Current Return on Equity (%)',
    'ROE_3Y_Avg': 'Average ROE over 3 years (%)',
    'ROE_5Y_Avg': 'Average ROE over 5 years (%)',

    # Risk Metrics (Red Flag Criteria)
    'Debt_Equity': 'Debt to Equity ratio',
    'Promoter_Holding': 'Promoter holding percentage (%)',
    'Pledged_Percentage': 'Promoter pledge percentage (%)',
    'Debt_3Y_vs_5Y_Ratio': 'Debt growth ratio (3Y debt/5Y debt)',

    # Analysis Results
    'Red_Flag_Count': 'Number of risk red flags (0-7)',
    'Green_Flag_Count': 'Number of quality green flags (0-11)',
    'Risk_Category': 'Risk level classification',
    'Quality_Grade': 'Quality grade classification',
    'Matrix_Classification': 'Combined risk-quality classification',
    'Recommended_Action': 'Investment recommendation',

    # Portfolio Impact
    'Investment_Value': 'Original investment amount (₹)',
    'Current_Value': 'Current value (₹)',
    'Loss_Amount': 'Absolute loss amount (₹)'
}

# Quality Criteria (Green Flags) Explanation
quality_criteria = [
    "1. Current PE < Historical PE 5Years (Relatively undervalued)",
    "2. Current PE < Historical PE 3Years (Recent undervaluation)",
    "3. PEG Ratio < 2.0 (Growth at reasonable price)",
    "4. PE < 2 × EPS Growth 3Years (Growth-adjusted valuation)",
    "5. PE < 5 × EPS Growth 5Years (Long-term growth valuation)",
    "6. Market Cap > ₹300 Cr (Adequate size)",
    "7. Return over 1 year > 10% (Recent momentum)",
    "8. Return over 3 years > 10% (Sustained performance)",
    "9. Average ROE 3Years > 20% (High profitability)",
    "10. Average ROE 5Years > 20% (Consistent profitability)",
    "11. Current ROE > 12% (Adequate current returns)"
]

# Risk Criteria (Red Flags) Explanation
risk_criteria = [
    "1. Average ROE 3Years < 10% (Poor profitability)",
    "2. Debt to Equity > 1.0 (High leverage)",
    "3. Promoter Holding < 20% (Low promoter commitment)",
    "4. Pledged Percentage > 30% (High promoter stress)",
    "5. Debt increasing trend (Rising financial risk)",
    "6. Stock Return 3Years < 10% (Poor long-term performance)",
    "7. Stock Return 1Year < 10% (Poor recent performance)"
]

print("📊 DATA PARAMETER EXPLANATIONS:")
print()
print("BASIC INFORMATION:")
for key in ['Symbol', 'Company_Name', 'Sector', 'Market_Cap', 'Portfolio_Weight', 'Current_Loss_Pct']:
    print(f"• {key}: {parameter_explanations[key]}")
print()

print("VALUATION METRICS (Quality Assessment):")
for key in ['Current_PE', 'Historical_PE_5Y', 'Historical_PE_3Y', 'PEG_Ratio', 'EPS_Growth_3Y', 'EPS_Growth_5Y']:
    print(f"• {key}: {parameter_explanations[key]}")
print()

print("PERFORMANCE METRICS:")
for key in ['Return_1Y', 'Return_3Y', 'ROE_Current', 'ROE_3Y_Avg', 'ROE_5Y_Avg']:
    print(f"• {key}: {parameter_explanations[key]}")
print()

print("RISK METRICS (Red Flag Assessment):")
for key in ['Debt_Equity', 'Promoter_Holding', 'Pledged_Percentage', 'Debt_3Y_vs_5Y_Ratio']:
    print(f"• {key}: {parameter_explanations[key]}")
print()

print("ANALYSIS RESULTS:")
for key in ['Red_Flag_Count', 'Green_Flag_Count', 'Risk_Category', 'Quality_Grade', 'Matrix_Classification', 'Recommended_Action']:
    print(f"• {key}: {parameter_explanations[key]}")
print()

print("PORTFOLIO IMPACT:")
for key in ['Investment_Value', 'Current_Value', 'Loss_Amount']:
    print(f"• {key}: {parameter_explanations[key]}")
print()

print("=" * 80)
print("QUALITY CRITERIA (GREEN FLAGS)")
print("=" * 80)
print()
for criterion in quality_criteria:
    print(criterion)
print()

print("=" * 80)
print("RISK CRITERIA (RED FLAGS)")
print("=" * 80)
print()
for criterion in risk_criteria:
    print(criterion)
print()

# Load and display sample of the CSV data
try:
    df = pd.read_csv('/Users/mitul/algo/comprehensive_stock_analysis_data.csv')

    print("=" * 80)
    print("CSV FILE SAMPLE (First 5 columns)")
    print("=" * 80)
    print()

    # Display first few columns to fit in console
    sample_cols = ['Symbol', 'Sector', 'Market_Cap', 'Portfolio_Weight', 'Current_Loss_Pct']
    print(df[sample_cols].to_string(index=False, float_format='%.2f'))
    print()

    print("=" * 80)
    print("KEY METRICS SAMPLE")
    print("=" * 80)
    print()

    key_cols = ['Symbol', 'Current_PE', 'PEG_Ratio', 'ROE_Current', 'Red_Flag_Count', 'Green_Flag_Count']
    print(df[key_cols].to_string(index=False, float_format='%.2f'))
    print()

    print("=" * 80)
    print("ANALYSIS RESULTS SAMPLE")
    print("=" * 80)
    print()

    result_cols = ['Symbol', 'Risk_Category', 'Quality_Grade', 'Recommended_Action']
    print(df[result_cols].to_string(index=False))
    print()

    print(f"✅ CSV file successfully created with {len(df)} stocks and {len(df.columns)} parameters")
    print("📁 File location: /Users/mitul/algo/comprehensive_stock_analysis_data.csv")
    print()

    print("📊 SUMMARY STATISTICS:")
    print(f"• Average Red Flags: {df['Red_Flag_Count'].mean():.1f}")
    print(f"• Average Green Flags: {df['Green_Flag_Count'].mean():.1f}")
    print(f"• Stocks with 5+ Red Flags: {len(df[df['Red_Flag_Count'] >= 5])}")
    print(f"• Stocks with 7+ Green Flags: {len(df[df['Green_Flag_Count'] >= 7])}")
    print(f"• Total Portfolio Loss: ₹{df['Loss_Amount'].sum():,.0f}")

except FileNotFoundError:
    print("❌ CSV file not found. Please ensure the file was created successfully.")

print()
print("=" * 80)
print("HOW TO USE THE CSV FILE")
print("=" * 80)
print()

print("📈 EXCEL/SHEETS ANALYSIS:")
print("• Import the CSV into Excel or Google Sheets")
print("• Use filters to sort by Red_Flag_Count (ascending) and Green_Flag_Count (descending)")
print("• Create pivot tables to analyze by Sector, Risk_Category, Quality_Grade")
print("• Use conditional formatting to highlight high-risk (Red_Flag_Count ≥ 5)")
print("• Create charts to visualize Portfolio_Weight vs Current_Loss_Pct")
print()

print("🔍 KEY ANALYSIS QUERIES:")
print("• Which stocks have Red_Flag_Count ≤ 2 AND Green_Flag_Count ≥ 7? (Best holdings)")
print("• Which stocks have Red_Flag_Count ≥ 5? (Immediate exit candidates)")
print("• What's the correlation between PEG_Ratio and recent returns?")
print("• Which sectors have the highest average Red_Flag_Count?")
print("• How does Debt_Equity correlate with ROE_Current?")
print()

print("📊 PORTFOLIO OPTIMIZATION:")
print("• Sort by Matrix_Classification to see systematic action plan")
print("• Filter by Recommended_Action = 'STRONG BUY/INCREASE' for quality stocks")
print("• Calculate new portfolio weights after following recommendations")
print("• Track progress by re-running analysis quarterly")
print()

print("💡 TIP: Use this data for systematic, objective investment decisions")
print("    based on quantitative criteria rather than emotions or market sentiment!")

# Create a separate metadata file
metadata = {
    'File_Name': 'comprehensive_stock_analysis_data.csv',
    'Creation_Date': '2026-01-14',
    'Total_Stocks': 13,
    'Total_Parameters': 29,
    'Risk_Criteria_Count': 7,
    'Quality_Criteria_Count': 11,
    'Portfolio_Total_Investment': 3669679,
    'Portfolio_Current_Value': 2601656,
    'Portfolio_Total_Loss': 1068023,
    'Analysis_Framework': 'Dual Risk-Quality Matrix'
}

# Save metadata
with open('/Users/mitul/algo/csv_metadata.txt', 'w') as f:
    f.write("COMPREHENSIVE STOCK ANALYSIS CSV - METADATA\n")
    f.write("=" * 50 + "\n\n")
    for key, value in metadata.items():
        f.write(f"{key}: {value}\n")
    f.write("\nGenerated by Enhanced Fundamental Analysis Framework\n")

print()
print("📝 Additional metadata file created: csv_metadata.txt")