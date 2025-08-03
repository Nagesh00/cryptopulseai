"""
CryptoPulse AI - Minimal Test Server
Tests Flask routing and API endpoints
"""
from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>🚀 CryptoPulse AI - Debug Mode</h1><p>Server is running!</p><a href='/test-api'>Test APIs</a>"

@app.route('/test-api')
def test_api():
    results = {}
    
    # Test CoinGecko
    try:
        response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd", timeout=5)
        if response.status_code == 200:
            price = response.json()['bitcoin']['usd']
            results['coingecko'] = f"✅ Working - BTC: ${price:,.2f}"
        else:
            results['coingecko'] = f"❌ Error: {response.status_code}"
    except Exception as e:
        results['coingecko'] = f"❌ Error: {str(e)}"
    
    # Test Binance
    try:
        response = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=5)
        if response.status_code == 200:
            price = float(response.json()['price'])
            results['binance'] = f"✅ Working - BTC: ${price:,.2f}"
        else:
            results['binance'] = f"❌ Error: {response.status_code}"
    except Exception as e:
        results['binance'] = f"❌ Error: {str(e)}"
    
    html = "<h2>🔍 API Test Results</h2>"
    for api, result in results.items():
        html += f"<p><strong>{api.title()}:</strong> {result}</p>"
    
    return html

if __name__ == '__main__':
    print("🚀 Starting CryptoPulse AI Debug Server...")
    print("🌐 Open: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
