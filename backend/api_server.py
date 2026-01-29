#!/usr/bin/env python3
"""
Flask API Server for Stock Portfolio Analysis
Connects React frontend with Python analysis backend
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import os
import traceback
from datetime import datetime
import json

# Import our analysis modules
import sys
sys.path.append('/Users/mitul/portfolioanalyzer/backend')

# Import analysis functions (we'll need to modify these to return structured data)
# from portfolio_analysis import analyze_portfolio
# from enhanced_fundamental_checkpoint_analysis import analyze_risk_checkpoints
# from valuation_quality_screening import analyze_quality_metrics
# from comprehensive_risk_vs_quality_analysis import comprehensive_analysis

app = Flask(__name__)
CORS(app)  # Enable cross-origin requests from React

# Configuration
UPLOAD_FOLDER = '/Users/mitul/portfolioanalyzer/backend/uploads'
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if uploaded file has allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_portfolio_file(file_path):
    """
    Process uploaded portfolio file and extract stock data
    Returns standardized portfolio data structure
    """
    try:
        # Read the file based on extension
        if file_path.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file_path)
        elif file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            raise ValueError("Unsupported file format")

        # Standardize column names (handle variations in user files)
        column_mapping = {
            'symbol': ['Symbol', 'Stock', 'Ticker', 'Company', 'Stock Symbol'],
            'quantity': ['Quantity', 'Qty', 'Shares', 'Units'],
            'avg_price': ['Avg Price', 'Average Price', 'Buy Price', 'Purchase Price'],
            'current_price': ['Current Price', 'LTP', 'Market Price', 'Price'],
            'investment': ['Investment', 'Invested Amount', 'Cost'],
            'current_value': ['Current Value', 'Market Value', 'Value'],
            'pnl': ['P&L', 'PnL', 'Profit/Loss', 'Gain/Loss']
        }

        # Normalize column names
        df_clean = df.copy()
        df_clean.columns = df_clean.columns.str.strip()

        # Map columns to standard names
        for standard_name, variations in column_mapping.items():
            for col in df_clean.columns:
                if col in variations:
                    df_clean = df_clean.rename(columns={col: standard_name})
                    break

        # Extract portfolio data
        portfolio_data = []
        for _, row in df_clean.iterrows():
            stock_data = {
                'symbol': str(row.get('symbol', 'UNKNOWN')).upper(),
                'quantity': float(row.get('quantity', 0)),
                'avg_price': float(row.get('avg_price', 0)),
                'current_price': float(row.get('current_price', 0)),
                'investment': float(row.get('investment', 0)),
                'current_value': float(row.get('current_value', 0)),
                'pnl': float(row.get('pnl', 0))
            }
            portfolio_data.append(stock_data)

        return portfolio_data

    except Exception as e:
        raise Exception(f"Error processing file: {str(e)}")

def mock_analysis_pipeline(portfolio_data):
    """
    Mock analysis pipeline that simulates the backend analysis
    In production, this would call the actual analysis functions
    """

    # Calculate portfolio summary
    total_investment = sum(stock['investment'] for stock in portfolio_data)
    total_current_value = sum(stock['current_value'] for stock in portfolio_data)
    total_pnl = sum(stock['pnl'] for stock in portfolio_data)

    # Mock sector allocation based on common Indian stock sectors
    sector_mapping = {
        'RELIANCE': 'Energy & Utilities',
        'TCS': 'Information Technology',
        'INFY': 'Information Technology',
        'HDFC': 'Banking & Financial',
        'ICICIBANK': 'Banking & Financial',
        'KOTAKBANK': 'Banking & Financial',
        'HINDUNILVR': 'Fast Moving Consumer Goods',
        'NESTLEIND': 'Fast Moving Consumer Goods',
        'ASIANPAINT': 'Fast Moving Consumer Goods',
        'MARUTI': 'Automotive',
        'TATAMOTORS': 'Automotive',
        'BAJFINANCE': 'Banking & Financial',
        'SCILAL': 'Shipping & Logistics'
    }

    # Calculate sector allocation
    sector_values = {}
    for stock in portfolio_data:
        sector = sector_mapping.get(stock['symbol'], 'Others')
        if sector not in sector_values:
            sector_values[sector] = 0
        sector_values[sector] += stock['current_value']

    # Convert to percentages
    sector_allocation = []
    colors = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#06B6D4', '#F97316']
    for i, (sector, value) in enumerate(sector_values.items()):
        percentage = round((value / total_current_value) * 100, 1)
        sector_allocation.append({
            'sector': sector,
            'percentage': percentage,
            'color': colors[i % len(colors)]
        })

    # Mock risk-quality matrix data
    risk_quality_matrix = []
    for stock in portfolio_data:
        # Simulate quality and risk scores
        quality_score = np.random.uniform(3, 9)
        risk_score = np.random.uniform(1, 7)

        # Adjust based on performance
        if stock['pnl'] > 0:
            quality_score += 1
            risk_score -= 0.5
        else:
            quality_score -= 0.5
            risk_score += 1

        risk_quality_matrix.append({
            'symbol': stock['symbol'],
            'quality': round(quality_score, 1),
            'risk': round(max(1, risk_score), 1)
        })

    # Calculate risk distribution
    high_risk_count = sum(1 for item in risk_quality_matrix if item['risk'] > 5)
    medium_risk_count = sum(1 for item in risk_quality_matrix if 3 <= item['risk'] <= 5)
    low_risk_count = len(risk_quality_matrix) - high_risk_count - medium_risk_count

    total_stocks = len(risk_quality_matrix)
    risk_distribution = {
        'highRisk': round((high_risk_count / total_stocks) * 100, 1),
        'mediumRisk': round((medium_risk_count / total_stocks) * 100, 1),
        'lowRisk': round((low_risk_count / total_stocks) * 100, 1)
    }

    return {
        'totalStocks': total_stocks,
        'totalInvested': total_investment,
        'currentValue': total_current_value,
        'totalLoss': total_pnl,  # Can be negative (loss) or positive (gain)
        'riskScore': round(75 - (total_pnl / total_investment) * 100, 1),  # Higher loss = lower score
        'riskDistribution': risk_distribution,
        'stocksMatrix': risk_quality_matrix,
        'sectorAllocation': sector_allocation
    }

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'Stock Portfolio Analysis API'
    })

@app.route('/api/analyze', methods=['POST'])
def analyze_portfolio():
    """
    Analyze uploaded portfolio file
    """
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Please upload CSV or Excel file.'}), 400

        # Save uploaded file
        filename = f"portfolio_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        # Process the file
        portfolio_data = process_portfolio_file(file_path)

        # Run analysis pipeline
        analysis_results = mock_analysis_pipeline(portfolio_data)

        # Clean up uploaded file
        os.remove(file_path)

        return jsonify({
            'success': True,
            'data': analysis_results,
            'message': f'Successfully analyzed portfolio with {len(portfolio_data)} stocks'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'trace': traceback.format_exc()
        }), 500

@app.route('/api/demo-data', methods=['GET'])
def get_demo_data():
    """
    Return demo/mock data for testing frontend without file upload
    """
    demo_portfolio = [
        {'symbol': 'RELIANCE', 'quantity': 100, 'avg_price': 2500, 'current_price': 2400, 'investment': 250000, 'current_value': 240000, 'pnl': -10000},
        {'symbol': 'TCS', 'quantity': 50, 'avg_price': 3200, 'current_price': 3500, 'investment': 160000, 'current_value': 175000, 'pnl': 15000},
        {'symbol': 'INFY', 'quantity': 200, 'avg_price': 1500, 'current_price': 1600, 'investment': 300000, 'current_value': 320000, 'pnl': 20000},
    ]

    analysis_results = mock_analysis_pipeline(demo_portfolio)

    return jsonify({
        'success': True,
        'data': analysis_results,
        'message': 'Demo analysis data'
    })

if __name__ == '__main__':
    print("🚀 Starting Stock Portfolio Analysis API Server...")
    print(f"📁 Upload folder: {UPLOAD_FOLDER}")
    print(f"🌐 Server will be available at: http://localhost:5000")
    print(f"📊 Frontend should connect to: http://localhost:5000/api/")

    app.run(debug=True, host='0.0.0.0', port=5000)