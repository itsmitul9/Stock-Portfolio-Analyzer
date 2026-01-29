#!/usr/bin/env python3
"""
Basic HTTP API Server for Stock Portfolio Analysis
Compatible with Python 3.13+ (no deprecated modules)
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import urllib.parse
from datetime import datetime
import pandas as pd
import traceback
import tempfile

# Server configuration
HOST = 'localhost'
PORT = 5000
UPLOAD_DIR = '/Users/mitul/portfolioanalyzer/backend/uploads'

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

class PortfolioAPIHandler(BaseHTTPRequestHandler):
    """HTTP Request Handler for Portfolio Analysis API"""

    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_headers()
        self.end_headers()

    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/api/health':
            self.handle_health_check()
        elif self.path == '/api/demo-data':
            self.handle_demo_data()
        else:
            self.send_error(404, "Endpoint not found")

    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/api/analyze':
            self.handle_file_analysis()
        else:
            self.send_error(404, "Endpoint not found")

    def send_headers(self):
        """Send CORS headers for React frontend"""
        self.send_header('Access-Control-Allow-Origin', 'http://localhost:3001')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Content-type', 'application/json')

    def send_json_response(self, data, status_code=200):
        """Send JSON response with proper headers"""
        self.send_response(status_code)
        self.send_headers()
        self.end_headers()

        json_data = json.dumps(data, indent=2).encode('utf-8')
        self.wfile.write(json_data)

    def handle_health_check(self):
        """Health check endpoint"""
        response = {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'service': 'Basic Stock Portfolio Analysis API',
            'message': 'Server running successfully',
            'python_version': f"{os.sys.version.split()[0]}"
        }
        self.send_json_response(response)

    def handle_demo_data(self):
        """Return demo analysis data"""
        demo_data = self.generate_mock_analysis()
        response = {
            'success': True,
            'data': demo_data,
            'message': 'Demo analysis data generated'
        }
        self.send_json_response(response)

    def handle_file_analysis(self):
        """Handle file upload and analysis (simplified)"""
        try:
            # For now, return demo data with a message about file upload
            # In a production environment, you'd use a proper multipart parser
            demo_data = self.generate_mock_analysis()

            response = {
                'success': True,
                'data': demo_data,
                'message': 'File analysis completed (using demo data for now)',
                'note': 'File upload processing will be enhanced in production version'
            }
            self.send_json_response(response)

        except Exception as e:
            error_response = {
                'success': False,
                'error': str(e),
                'trace': traceback.format_exc()
            }
            self.send_json_response(error_response, 500)

    def generate_mock_analysis(self, portfolio_data=None):
        """Generate mock analysis data"""
        if not portfolio_data:
            # Default portfolio based on your previous data
            portfolio_data = [
                {'symbol': 'RELIANCE', 'investment': 250000, 'current_value': 240000, 'pnl': -10000},
                {'symbol': 'TCS', 'investment': 160000, 'current_value': 175000, 'pnl': 15000},
                {'symbol': 'INFY', 'investment': 300000, 'current_value': 320000, 'pnl': 20000},
                {'symbol': 'HDFC', 'investment': 200000, 'current_value': 195000, 'pnl': -5000},
                {'symbol': 'ICICIBANK', 'investment': 150000, 'current_value': 160000, 'pnl': 10000},
                {'symbol': 'KOTAKBANK', 'investment': 180000, 'current_value': 175000, 'pnl': -5000},
                {'symbol': 'HINDUNILVR', 'investment': 220000, 'current_value': 235000, 'pnl': 15000},
                {'symbol': 'ASIANPAINT', 'investment': 190000, 'current_value': 185000, 'pnl': -5000},
                {'symbol': 'MARUTI', 'investment': 170000, 'current_value': 165000, 'pnl': -5000},
                {'symbol': 'NESTLEIND', 'investment': 140000, 'current_value': 155000, 'pnl': 15000},
                {'symbol': 'SCILAL', 'investment': 50000, 'current_value': 35000, 'pnl': -15000},
                {'symbol': 'TATAMOTORS', 'investment': 80000, 'current_value': 70000, 'pnl': -10000},
                {'symbol': 'BAJFINANCE', 'investment': 120000, 'current_value': 130000, 'pnl': 10000}
            ]

        # Calculate summary metrics
        total_investment = sum(stock['investment'] for stock in portfolio_data)
        total_current_value = sum(stock['current_value'] for stock in portfolio_data)
        total_pnl = sum(stock['pnl'] for stock in portfolio_data)

        # Sector allocation based on your portfolio
        sector_allocation = [
            {'sector': 'Information Technology', 'percentage': 28.5, 'color': '#3B82F6'},
            {'sector': 'Banking & Financial', 'percentage': 24.2, 'color': '#10B981'},
            {'sector': 'Fast Moving Consumer Goods', 'percentage': 18.3, 'color': '#F59E0B'},
            {'sector': 'Automotive', 'percentage': 12.7, 'color': '#EF4444'},
            {'sector': 'Energy & Utilities', 'percentage': 8.9, 'color': '#8B5CF6'},
            {'sector': 'Pharmaceuticals', 'percentage': 4.2, 'color': '#06B6D4'},
            {'sector': 'Shipping & Logistics', 'percentage': 3.2, 'color': '#F97316'}
        ]

        # Risk-quality matrix with realistic data
        stocks_matrix = [
            {'symbol': 'RELIANCE', 'quality': 8.5, 'risk': 2.3},
            {'symbol': 'TCS', 'quality': 9.2, 'risk': 1.8},
            {'symbol': 'HDFC', 'quality': 7.8, 'risk': 3.1},
            {'symbol': 'INFY', 'quality': 8.7, 'risk': 2.0},
            {'symbol': 'ICICIBANK', 'quality': 7.2, 'risk': 4.2},
            {'symbol': 'KOTAKBANK', 'quality': 8.0, 'risk': 3.5},
            {'symbol': 'HINDUNILVR', 'quality': 9.0, 'risk': 1.5},
            {'symbol': 'ASIANPAINT', 'quality': 8.3, 'risk': 2.8},
            {'symbol': 'MARUTI', 'quality': 7.5, 'risk': 3.7},
            {'symbol': 'NESTLEIND', 'quality': 9.1, 'risk': 1.4},
            {'symbol': 'SCILAL', 'quality': 4.2, 'risk': 6.8},
            {'symbol': 'TATAMOTORS', 'quality': 5.5, 'risk': 5.9},
            {'symbol': 'BAJFINANCE', 'quality': 6.8, 'risk': 4.8}
        ]

        # Risk distribution calculation
        high_risk = len([s for s in stocks_matrix if s['risk'] > 5])
        medium_risk = len([s for s in stocks_matrix if 3 <= s['risk'] <= 5])
        low_risk = len(stocks_matrix) - high_risk - medium_risk

        total_stocks = len(stocks_matrix)
        risk_distribution = {
            'highRisk': round((high_risk / total_stocks) * 100, 1),
            'mediumRisk': round((medium_risk / total_stocks) * 100, 1),
            'lowRisk': round((low_risk / total_stocks) * 100, 1)
        }

        # Calculate risk score based on portfolio performance
        portfolio_return = (total_pnl / total_investment) * 100
        risk_score = max(0, min(100, 60 + portfolio_return * 2))

        return {
            'totalStocks': total_stocks,
            'totalInvested': int(total_investment),
            'currentValue': int(total_current_value),
            'totalLoss': int(total_pnl),
            'riskScore': round(risk_score, 1),
            'riskDistribution': risk_distribution,
            'stocksMatrix': stocks_matrix,
            'sectorAllocation': sector_allocation
        }

def run_server():
    """Start the API server"""
    server_address = (HOST, PORT)
    httpd = HTTPServer(server_address, PortfolioAPIHandler)

    print(f"🚀 Starting Basic Portfolio Analysis API Server...")
    print(f"🌐 Server running at: http://{HOST}:{PORT}")
    print(f"📊 Health check: http://{HOST}:{PORT}/api/health")
    print(f"🔗 Demo data: http://{HOST}:{PORT}/api/demo-data")
    print(f"📁 File analysis: POST to http://{HOST}:{PORT}/api/analyze")
    print(f"📂 Upload folder: {UPLOAD_DIR}")
    print("\n💡 This basic server provides demo data for testing.")
    print("   File upload will be enhanced with Flask in production.")
    print("\nPress Ctrl+C to stop the server")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        httpd.server_close()

if __name__ == '__main__':
    run_server()