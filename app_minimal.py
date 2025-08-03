#!/usr/bin/env python3
"""
CryptoPulse AI - Minimal Working Version
Simplified version to debug and test core functionality
"""

from flask import Flask, render_template, jsonify
import requests
import json
import os

app = Flask(__name__)

# Simple data storage
def read_data():
    try:
        with open('data.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "featured_article": {
                "title": "Welcome to CryptoPulse AI",
                "summary": "Real-time cryptocurrency dashboard with AI insights",
                "content": "Your dashboard is loading...",
                "image_url": "https://images.pexels.com/photos/730547/pexels-photo-730547.jpeg"
            },
            "news_articles": []
        }

@app.route("/")
def home():
    """Homepage with market data and news"""
    app_data = read_data()
    return render_template('index.html', 
                         featured_article=app_data.get('featured_article', {}), 
                         news_articles=app_data.get('news_articles', []))

@app.route("/coin/<symbol>")
def coin_detail(symbol):
    """Coin detail page with charts"""
    return render_template('coin_detail.html', symbol=symbol)

@app.route("/api/market-data")
def get_market_data():
    """Live market data API"""
    try:
        # Try CoinGecko first (most reliable)
        response = requests.get(
            "https://api.coingecko.com/api/v3/coins/markets",
            params={
                'vs_currency': 'usd',
                'order': 'market_cap_desc',
                'per_page': 50,
                'page': 1,
                'sparkline': False,
                'price_change_percentage': '24h'
            },
            timeout=10
        )
        
        if response.status_code == 200:
            coingecko_data = response.json()
            
            # Convert to format expected by frontend
            formatted_data = []
            for coin in coingecko_data:
                formatted_data.append({
                    'symbol': f"{coin['symbol'].upper()}USDT",
                    'lastPrice': f"{coin['current_price']:.6f}",
                    'priceChangePercent': f"{coin.get('price_change_percentage_24h', 0):.2f}",
                    'volume': f"{coin.get('total_volume', 0):.0f}",
                    'quoteVolume': f"{coin.get('market_cap', 0):.0f}",
                    'weightedAvgPrice': f"{coin['current_price']:.6f}"
                })
            
            return jsonify(formatted_data)
        
    except Exception as e:
        print(f"CoinGecko API error: {e}")
    
    # Fallback data if APIs fail
    fallback_data = [
        {
            'symbol': 'BTCUSDT',
            'lastPrice': '113835.00',
            'priceChangePercent': '0.10',
            'volume': '25000000',
            'quoteVolume': '1500000000',
            'weightedAvgPrice': '113500.00'
        },
        {
            'symbol': 'ETHUSDT',
            'lastPrice': '3485.23',
            'priceChangePercent': '-0.50',
            'volume': '15000000',
            'quoteVolume': '800000000',
            'weightedAvgPrice': '3480.00'
        }
    ]
    
    return jsonify(fallback_data)

@app.route("/api/kline-data/<symbol>")
def get_kline_data(symbol):
    """Chart data for coins"""
    try:
        # Simple fallback chart data
        import random
        from datetime import datetime, timedelta
        
        data = []
        base_price = 50000 if symbol == 'BTC' else 3000
        
        for i in range(30):  # 30 days of data
            date = datetime.now() - timedelta(days=29-i)
            price_variation = random.uniform(0.95, 1.05)
            price = base_price * price_variation
            
            data.append({
                "time": int(date.timestamp()),
                "open": round(price * 0.99, 2),
                "high": round(price * 1.02, 2),
                "low": round(price * 0.97, 2),
                "close": round(price, 2)
            })
            
            base_price = price  # Update for next day
        
        return jsonify(data)
        
    except Exception as e:
        print(f"Chart data error: {e}")
        return jsonify([])

@app.route("/test")
def test():
    """Test endpoint"""
    return "<h1>✅ CryptoPulse AI is working!</h1><p>Flask server is running correctly.</p>"

if __name__ == '__main__':
    print("🚀 Starting CryptoPulse AI (Minimal Version)...")
    print("🌐 Server will be available at: http://localhost:5000")
    print("✨ Test endpoint: http://localhost:5000/test")
    
    # Start Flask
    app.run(debug=True, host='0.0.0.0', port=5000)
