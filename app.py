import requests
import json
import atexit
import os
from datetime import datetime
from flask import Flask, render_template, jsonify
from apscheduler.schedulers.background import BackgroundScheduler

# Configuration - Use environment variables in production, fallback to config.py for local development
try:
    from config import NEWS_API_KEY, AI_API_KEY, PEXELS_API_KEY
except ImportError:
    # Use environment variables if config.py is not available (production)
    NEWS_API_KEY = os.environ.get('NEWS_API_KEY', '')
    AI_API_KEY = os.environ.get('AI_API_KEY', '')
    PEXELS_API_KEY = os.environ.get('PEXELS_API_KEY', '')

# --- FLASK APP INITIALIZATION ---
app = Flask(__name__)

# --- API ENDPOINTS ---
BINANCE_API_URL = "https://api.binance.com/api/v3"
COINGECKO_API_URL = "https://api.coingecko.com/api/v3"
NEWS_API_URL = "https://newsapi.org/v2/top-headlines"
PEXELS_API_URL = "https://api.pexels.com/v1/search"
# Gemini API endpoint
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent" 

# --- DATA PERSISTENCE ---
DATA_FILE = "data.json"

def read_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Return a default structure if the file is missing or corrupt
        return {"featured_article": {}, "news_articles": []}

def write_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# --- AUTOMATED TASKS (SCHEDULER) ---

# Task 1: Fetch trending news articles
def fetch_latest_news():
    print(f"[{datetime.now()}] Running scheduled task: Fetching news...")
    params = {
        'apiKey': NEWS_API_KEY,
        'category': 'business',
        'language': 'en',
        'sortBy': 'publishedAt',
        'pageSize': 10 
    }
    try:
        response = requests.get(NEWS_API_URL, params=params)
        response.raise_for_status()
        news_data = response.json().get('articles', [])
        
        # Format and save news
        current_data = read_data()
        current_data['news_articles'] = [
            {
                "source": article['source']['name'],
                "title": article['title'],
                "url": article['url'],
                "image_url": article.get('urlToImage', 'https://via.placeholder.com/150'),
                "published_at": article['publishedAt']
            } for article in news_data
        ]
        write_data(current_data)
        print("News fetching completed successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")

def generate_daily_article():
    print(f"[{datetime.now()}] Running scheduled task: Generating AI article...")
    try:
        # Step 1: Try to identify a trending topic (e.g., top gainer)
        try:
            market_data = requests.get(f"{BINANCE_API_URL}/ticker/24hr", timeout=10).json()
            # Find a coin with significant movement (e.g., top gainer)
            top_gainer = sorted([coin for coin in market_data if coin['symbol'].endswith('USDT')], 
                                  key=lambda x: float(x['priceChangePercent']), 
                                  reverse=True)[0]
            topic = f"{top_gainer['symbol'].replace('USDT','')} ({top_gainer['priceChangePercent']}% move)"
        except Exception as api_error:
            print(f"Binance API timeout, using fallback topic: {api_error}")
            # Fallback topic when API is unavailable
            import random
            fallback_topics = [
                "Bitcoin (BTC) market analysis",
                "Ethereum (ETH) price movement", 
                "Cryptocurrency market trends",
                "DeFi ecosystem developments",
                "Altcoin season analysis"
            ]
            topic = random.choice(fallback_topics)
        
        print(f"Identified trending topic: {topic}")

        # Step 2: Generate content with Gemini AI
        ai_prompt = f"Write a 500-word blog post about {topic}. Discuss potential factors and market sentiment. Make it informative and engaging for cryptocurrency investors."
        print(f"AI Prompt: {ai_prompt}")
        
        try:
            # Call Gemini API
            gemini_payload = {
                "contents": [{
                    "parts": [{
                        "text": ai_prompt
                    }]
                }]
            }
            
            gemini_response = requests.post(
                f"{GEMINI_API_URL}?key={AI_API_KEY}",
                json=gemini_payload,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            gemini_response.raise_for_status()
            
            generated_content = gemini_response.json()['candidates'][0]['content']['parts'][0]['text']
            generated_title = f"Market Analysis: {topic.split('(')[0].strip()}"
            generated_summary = " ".join(generated_content.split(' ')[:30]) + "..."
            
        except Exception as ai_error:
            print(f"AI API error: {ai_error}")
            # Fallback content
            generated_title = f"Market Analysis: {topic.split('(')[0].strip()}"
            generated_content = f"The cryptocurrency market continues to show interesting developments with {topic}. Market participants are closely monitoring price movements and trading volumes across major digital assets. Current market conditions suggest a mix of bullish and bearish sentiment, with institutional interest remaining strong. Technical analysis indicates potential support and resistance levels that traders should watch. Risk management remains crucial in these volatile market conditions."
            generated_summary = " ".join(generated_content.split(' ')[:30]) + "..."
        
        # Step 3: Fetch a relevant image from Pexels
        image_search_term = topic.split(' ')[0] + " cryptocurrency"
        print(f"Pexels search term: {image_search_term}")
        
        try:
            headers = {'Authorization': PEXELS_API_KEY}
            params = {'query': image_search_term, 'per_page': 1}
            pexels_response = requests.get(PEXELS_API_URL, headers=headers, params=params)
            pexels_response.raise_for_status()
            
            pexels_data = pexels_response.json()
            if pexels_data['photos']:
                image_url = pexels_data['photos'][0]['src']['large2x']
            else:
                # Fallback to crypto-related image
                image_url = "https://images.pexels.com/photos/730547/pexels-photo-730547.jpeg"
                
        except Exception as img_error:
            print(f"Pexels API error: {img_error}")
            # Fallback image
            image_url = "https://images.pexels.com/photos/730547/pexels-photo-730547.jpeg"

        # Step 4: Save the new article
        current_data = read_data()
        current_data['featured_article'] = {
            "title": generated_title,
            "summary": generated_summary,
            "content": generated_content, # In a real app, save full content
            "image_url": image_url
        }
        write_data(current_data)
        print("AI article generation completed successfully.")

    except Exception as e:
        print(f"Error generating daily article: {e}")

# --- FLASK ROUTES ---

@app.route("/")
def home():
    """Renders the homepage with the latest market data, news, and featured article."""
    app_data = read_data()
    return render_template('index.html', 
                           featured_article=app_data.get('featured_article'), 
                           news_articles=app_data.get('news_articles'))

@app.route("/coin/<symbol>")
def coin_detail(symbol):
    """Renders the detailed page for a specific cryptocurrency."""
    return render_template('coin_detail.html', symbol=symbol)

# --- API ENDPOINTS FOR FRONTEND ---

@app.route("/api/market-data")
def get_market_data():
    """Provides live market data for the top 100 coins."""
    
    # Try CoinGecko API first (no API key required, more reliable)
    try:
        print("Trying CoinGecko API...")
        response = requests.get(
            f"{COINGECKO_API_URL}/coins/markets",
            params={
                'vs_currency': 'usd',
                'order': 'market_cap_desc',
                'per_page': 100,
                'page': 1,
                'sparkline': False,
                'price_change_percentage': '24h'
            },
            timeout=10
        )
        response.raise_for_status()
        coingecko_data = response.json()
        
        # Convert CoinGecko format to our expected format
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
        
        print(f"✅ CoinGecko API success: {len(formatted_data)} coins")
        return jsonify(formatted_data)
        
    except Exception as coingecko_error:
        print(f"CoinGecko API error: {coingecko_error}")
    
    # Fallback to Binance API
    try:
        print("Trying Binance API...")
        response = requests.get(f"{BINANCE_API_URL}/ticker/24hr", timeout=5)
        response.raise_for_status()
        data = response.json()
        
        # Filter for USDT pairs and sort by volume
        usdt_pairs = [item for item in data if item['symbol'].endswith('USDT')]
        usdt_pairs.sort(key=lambda x: float(x.get('quoteVolume', 0)), reverse=True)
        
        print(f"✅ Binance API success: {len(usdt_pairs[:100])} coins")
        return jsonify(usdt_pairs[:100])
        
    except Exception as binance_error:
        print(f"Binance API error: {binance_error}")
    
    # Final fallback to simulated data
    print("Using fallback simulated data...")
    fallback_data = get_fallback_market_data()
    return jsonify(fallback_data)

def get_fallback_market_data():
    """Provides fallback market data when APIs are unavailable."""
    import random
    import time
    
    # Popular cryptocurrencies with simulated data
    popular_cryptos = [
        'BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'XRPUSDT', 'ADAUSDT', 
        'SOLUSDT', 'DOGEUSDT', 'DOTUSDT', 'AVAXUSDT', 'LTCUSDT',
        'LINKUSDT', 'ATOMUSDT', 'XLMUSDT', 'NEARUSDT', 'ALGOUSDT',
        'VETUSDT', 'ICPUSDT', 'FILUSDT', 'TRXUSDT', 'ETCUSDT'
    ]
    
    fallback_data = []
    base_prices = {
        'BTCUSDT': 45000, 'ETHUSDT': 2800, 'BNBUSDT': 320, 'XRPUSDT': 0.6,
        'ADAUSDT': 0.45, 'SOLUSDT': 90, 'DOGEUSDT': 0.08, 'DOTUSDT': 7.5,
        'AVAXUSDT': 25, 'LTCUSDT': 90, 'LINKUSDT': 15, 'ATOMUSDT': 10,
        'XLMUSDT': 0.12, 'NEARUSDT': 5, 'ALGOUSDT': 0.25, 'VETUSDT': 0.025,
        'ICPUSDT': 12, 'FILUSDT': 6, 'TRXUSDT': 0.08, 'ETCUSDT': 20
    }
    
    for symbol in popular_cryptos:
        base_price = base_prices.get(symbol, 100)
        # Add some random variation
        price_change = random.uniform(-10, 10)
        current_price = base_price * (1 + price_change / 100)
        
        fallback_data.append({
            'symbol': symbol,
            'lastPrice': f"{current_price:.6f}",
            'priceChangePercent': f"{price_change:.2f}",
            'volume': f"{random.randint(10000, 1000000)}",
            'quoteVolume': f"{random.randint(100000000, 1000000000)}",
            'weightedAvgPrice': f"{current_price * 0.99:.6f}"
        })
    
    return fallback_data

def get_top_100_symbols_by_market_cap():
    """Helper to get symbols, as Binance API requires them for batch requests."""
    # This is a simplified approach. A better way is to use an endpoint that lists all coins
    # and then filter, but for this example, we use a pre-compiled (but extensive) list.
    # In a real app, you might fetch this list periodically.
    response = requests.get(f"{BINANCE_API_URL}/ticker/24hr")
    all_tickers = response.json()
    usdt_tickers = [t for t in all_tickers if t['symbol'].endswith('USDT')]
    # Sort by a proxy for market cap: volume * price
    usdt_tickers.sort(key=lambda x: float(x.get('quoteVolume', 0)), reverse=True)
    return [t['symbol'].replace('USDT', '') for t in usdt_tickers[:100]]

@app.route("/api/kline-data/<symbol>")
def get_kline_data(symbol):
    """Provides historical k-line (candlestick) data for a given symbol."""
    
    # Try CoinGecko API first for historical data
    try:
        print(f"Getting chart data for {symbol} from CoinGecko...")
        
        # Get coin ID from symbol (simplified mapping)
        symbol_to_id = {
            'BTC': 'bitcoin', 'ETH': 'ethereum', 'BNB': 'binancecoin',
            'XRP': 'ripple', 'ADA': 'cardano', 'SOL': 'solana',
            'DOGE': 'dogecoin', 'DOT': 'polkadot', 'AVAX': 'avalanche-2',
            'LTC': 'litecoin', 'LINK': 'chainlink', 'ATOM': 'cosmos',
            'XLM': 'stellar', 'NEAR': 'near', 'ALGO': 'algorand',
            'VET': 'vechain', 'ICP': 'internet-computer', 'FIL': 'filecoin',
            'TRX': 'tron', 'ETC': 'ethereum-classic'
        }
        
        coin_id = symbol_to_id.get(symbol.upper(), symbol.lower())
        
        response = requests.get(
            f"{COINGECKO_API_URL}/coins/{coin_id}/ohlc",
            params={'vs_currency': 'usd', 'days': 100},
            timeout=10
        )
        response.raise_for_status()
        ohlc_data = response.json()
        
        # Format for TradingView Lightweight Charts
        formatted_data = []
        for candle in ohlc_data:
            formatted_data.append({
                "time": int(candle[0] / 1000),  # timestamp in seconds
                "open": float(candle[1]),
                "high": float(candle[2]),
                "low": float(candle[3]),
                "close": float(candle[4])
            })
        
        print(f"✅ CoinGecko chart data success: {len(formatted_data)} candles")
        return jsonify(formatted_data)
        
    except Exception as coingecko_error:
        print(f"CoinGecko chart API error: {coingecko_error}")
    
    # Fallback to Binance API
    params = {
        'symbol': f"{symbol}USDT",
        'interval': '1d',
        'limit': 100
    }
    try:
        print(f"Trying Binance API for {symbol}...")
        response = requests.get(f"{BINANCE_API_URL}/klines", params=params, timeout=10)
        response.raise_for_status()
        
        formatted_data = [
            {
                "time": int(k[0] / 1000),
                "open": float(k[1]),
                "high": float(k[2]),
                "low": float(k[3]),
                "close": float(k[4])
            } for k in response.json()
        ]
        
        print(f"✅ Binance chart data success: {len(formatted_data)} candles")
        return jsonify(formatted_data)
        
    except Exception as binance_error:
        print(f"Binance chart API error: {binance_error}")
    
    # Final fallback to generated data
    print(f"Using fallback chart data for {symbol}...")
    fallback_chart_data = get_fallback_chart_data(symbol)
    return jsonify(fallback_chart_data)

def get_fallback_chart_data(symbol):
    """Generate fallback chart data when API is unavailable."""
    import random
    import time
    from datetime import datetime, timedelta
    
    # Base prices for different symbols
    base_prices = {
        'BTC': 45000, 'ETH': 2800, 'BNB': 320, 'XRP': 0.6, 'ADA': 0.45,
        'SOL': 90, 'DOGE': 0.08, 'DOT': 7.5, 'AVAX': 25, 'LTC': 90
    }
    
    base_price = base_prices.get(symbol, 100)
    data = []
    
    # Generate 100 days of sample data
    for i in range(100):
        date = datetime.now() - timedelta(days=99-i)
        timestamp = int(date.timestamp())
        
        # Add some realistic price movement
        daily_change = random.uniform(-5, 5) / 100
        if i > 0:
            base_price = base_price * (1 + daily_change)
        
        # Generate OHLC data
        high = base_price * random.uniform(1.01, 1.05)
        low = base_price * random.uniform(0.95, 0.99)
        open_price = base_price * random.uniform(0.98, 1.02)
        close_price = base_price * random.uniform(0.98, 1.02)
        
        data.append({
            "time": timestamp,
            "open": round(open_price, 6),
            "high": round(high, 6),
            "low": round(low, 6),
            "close": round(close_price, 6)
        })
    
    return data

# --- SCHEDULER SETUP AND EXECUTION ---
if __name__ == '__main__':
    # Run tasks once on startup
    fetch_latest_news()
    generate_daily_article()

    # Configure scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=fetch_latest_news, trigger="interval", hours=1)
    scheduler.add_job(func=generate_daily_article, trigger="interval", hours=24)
    scheduler.start()

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())

    # Production-ready configuration
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
