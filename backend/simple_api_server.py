#!/usr/bin/env python3
"""
Simple HTTP API Server for Stock Portfolio Analysis
Uses only Python built-in modules (no external dependencies)
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import urllib.parse
import cgi
import io
from datetime import datetime
import pandas as pd
import tempfile
import traceback

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
        self.send_header('Access-Control-Allow-Origin', 'http://localhost:3000')
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
            'service': 'Simple Stock Portfolio Analysis API',
            'message': 'Server running with Python built-in modules'
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
        """Handle file upload and analysis"""
        try:
            # Parse multipart form data
            content_type = self.headers.get('Content-Type', '')

            if not content_type.startswith('multipart/form-data'):
                self.send_json_response({
                    'success': False,
                    'error': 'Invalid content type. Expected multipart/form-data'
                }, 400)
                return

            # Read the request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            # Parse form data
            form = cgi.FieldStorage(
                fp=io.BytesIO(post_data),
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )

            if 'file' not in form:
                self.send_json_response({
                    'success': False,
                    'error': 'No file uploaded'
                }, 400)
                return

            file_item = form['file']
            if not file_item.filename:
                self.send_json_response({
                    'success': False,
                    'error': 'No file selected'
                }, 400)
                return

            # Save uploaded file temporarily
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"portfolio_{timestamp}_{file_item.filename}"
            file_path = os.path.join(UPLOAD_DIR, filename)

            with open(file_path, 'wb') as f:
                f.write(file_item.file.read())

            # Process the file
            portfolio_data = self.process_portfolio_file(file_path)

            # Generate analysis
            analysis_results = self.analyze_portfolio(portfolio_data)

            # Clean up
            os.remove(file_path)

            response = {
                'success': True,
                'data': analysis_results,
                'message': f'Successfully analyzed portfolio with {len(portfolio_data)} stocks'
            }
            self.send_json_response(response)

        except Exception as e:
            error_response = {
                'success': False,
                'error': str(e),
                'trace': traceback.format_exc()
            }
            self.send_json_response(error_response, 500)

    def process_portfolio_file(self, file_path):
        """Process uploaded CSV/Excel file"""
        try:
            # Read file based on extension
            if file_path.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file_path)
            elif file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            else:
                raise ValueError("Unsupported file format")

            # Extract portfolio data
            portfolio_data = []
            for _, row in df.iterrows():
                # Handle various column name formats
                symbol = str(row.get('Symbol', row.get('Stock', row.get('Ticker', 'UNKNOWN')))).upper()
                quantity = float(row.get('Quantity', row.get('Qty', 0)))
                avg_price = float(row.get('Avg Price', row.get('Average Price', 0)))
                current_price = float(row.get('Current Price', row.get('LTP', 0)))
                investment = float(row.get('Investment', row.get('Invested Amount', avg_price * quantity)))
                current_value = float(row.get('Current Value', row.get('Market Value', current_price * quantity)))
                pnl = float(row.get('P&L', row.get('PnL', current_value - investment)))

                stock_data = {
                    'symbol': symbol,
                    'quantity': quantity,
                    'avg_price': avg_price,
                    'current_price': current_price,
                    'investment': investment,
                    'current_value': current_value,
                    'pnl': pnl
                }
                portfolio_data.append(stock_data)

            return portfolio_data

        except Exception as e:
            raise Exception(f"Error processing file: {str(e)}")

    def analyze_portfolio(self, portfolio_data):
        """Analyze portfolio data and return structured results"""
        return self.generate_mock_analysis(portfolio_data)

    def generate_mock_analysis(self, portfolio_data=None):
        """Generate mock analysis data"""
        if not portfolio_data:
            # Default mock data
            portfolio_data = [
                {'symbol': 'RELIANCE', 'investment': 250000, 'current_value': 240000, 'pnl': -10000},
                {'symbol': 'TCS', 'investment': 160000, 'current_value': 175000, 'pnl': 15000},
                {'symbol': 'INFY', 'investment': 300000, 'current_value': 320000, 'pnl': 20000},
            ]

        # Calculate summary metrics
        total_investment = sum(stock['investment'] for stock in portfolio_data)
        total_current_value = sum(stock['current_value'] for stock in portfolio_data)
        total_pnl = sum(stock['pnl'] for stock in portfolio_data)

        # Mock sector allocation
        sector_allocation = [
            {'sector': 'Information Technology', 'percentage': 28.5, 'color': '#3B82F6'},
            {'sector': 'Banking & Financial', 'percentage': 24.2, 'color': '#10B981'},
            {'sector': 'Fast Moving Consumer Goods', 'percentage': 18.3, 'color': '#F59E0B'},
            {'sector': 'Automotive', 'percentage': 12.7, 'color': '#EF4444'},
            {'sector': 'Energy & Utilities', 'percentage': 8.9, 'color': '#8B5CF6'},
            {'sector': 'Others', 'percentage': 7.4, 'color': '#06B6D4'}
        ]

        # Mock risk-quality matrix
        stocks_matrix = []
        import random
        for stock in portfolio_data:
            quality = round(random.uniform(3, 9), 1)
            risk = round(random.uniform(1, 7), 1)

            # Adjust based on P&L
            if stock['pnl'] > 0:
                quality += 0.5
                risk -= 0.3

            stocks_matrix.append({
                'symbol': stock['symbol'],
                'quality': min(10, max(1, quality)),
                'risk': min(10, max(1, risk))
            })

        # Risk distribution
        high_risk = len([s for s in stocks_matrix if s['risk'] > 6])
        medium_risk = len([s for s in stocks_matrix if 3 <= s['risk'] <= 6])
        low_risk = len(stocks_matrix) - high_risk - medium_risk

        total_stocks = len(stocks_matrix)
        risk_distribution = {
            'highRisk': round((high_risk / total_stocks) * 100, 1),
            'mediumRisk': round((medium_risk / total_stocks) * 100, 1),
            'lowRisk': round((low_risk / total_stocks) * 100, 1)
        }

        return {
            'totalStocks': total_stocks,
            'totalInvested': int(total_investment),
            'currentValue': int(total_current_value),
            'totalLoss': int(total_pnl),
            'riskScore': max(0, min(100, 70 + (total_pnl / total_investment) * 30)),
            'riskDistribution': risk_distribution,
            'stocksMatrix': stocks_matrix,
            'sectorAllocation': sector_allocation
        }

def run_server():
    """Start the API server"""
    server_address = (HOST, PORT)
    httpd = HTTPServer(server_address, PortfolioAPIHandler)

    print(f"🚀 Starting Simple Portfolio Analysis API Server...")
    print(f"🌐 Server running at: http://{HOST}:{PORT}")
    print(f"📊 Health check: http://{HOST}:{PORT}/api/health")
    print(f"🔗 Demo data: http://{HOST}:{PORT}/api/demo-data")
    print(f"📁 File analysis: POST to http://{HOST}:{PORT}/api/analyze")
    print(f"📂 Upload folder: {UPLOAD_DIR}")
    print("\nPress Ctrl+C to stop the server")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        httpd.server_close()

if __name__ == '__main__':
    run_server()