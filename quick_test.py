"""
Quick test of CryptoPulse AI core functions
"""
import sys
import os
sys.path.append(os.getcwd())

def test_api_endpoints():
    """Test individual API functions"""
    print("Testing CryptoPulse AI functions...")
    
    try:
        import requests
        from config import NEWS_API_KEY, AI_API_KEY, PEXELS_API_KEY
        print("✅ Config imported successfully")
        print(f"📡 APIs configured: NewsAPI={'✅' if NEWS_API_KEY else '❌'}, AI={'✅' if AI_API_KEY else '❌'}, Pexels={'✅' if PEXELS_API_KEY else '❌'}")
    except Exception as e:
        print(f"❌ Config import failed: {e}")
        return
    
    # Test Binance API
    print("\n🔍 Testing Binance Market Data...")
    try:
        response = requests.get("https://api.binance.com/api/v3/ticker/24hr", timeout=10)
        if response.status_code == 200:
            data = response.json()
            usdt_pairs = [item for item in data if item['symbol'].endswith('USDT')][:5]
            print(f"✅ Binance API working - {len(usdt_pairs)} USDT pairs found")
            for coin in usdt_pairs[:3]:
                print(f"   {coin['symbol']}: ${float(coin['lastPrice']):,.4f} ({coin['priceChangePercent']}%)")
        else:
            print(f"❌ Binance API failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Binance error: {e}")
    
    # Test CoinGecko API
    print("\n🔍 Testing CoinGecko API...")
    try:
        response = requests.get(
            "https://api.coingecko.com/api/v3/coins/markets",
            params={
                'vs_currency': 'usd',
                'order': 'market_cap_desc',
                'per_page': 5,
                'page': 1
            },
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ CoinGecko API working - {len(data)} coins retrieved")
            for coin in data[:3]:
                print(f"   {coin['symbol'].upper()}: ${coin['current_price']:,.4f} ({coin.get('price_change_percentage_24h', 0):.2f}%)")
        else:
            print(f"❌ CoinGecko API failed: {response.status_code}")
    except Exception as e:
        print(f"❌ CoinGecko error: {e}")
    
    # Test NewsAPI
    print("\n🔍 Testing NewsAPI...")
    try:
        params = {
            'apiKey': NEWS_API_KEY,
            'category': 'business',
            'language': 'en',
            'pageSize': 3
        }
        response = requests.get("https://newsapi.org/v2/top-headlines", params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            print(f"✅ NewsAPI working - {len(articles)} articles found")
            for article in articles[:2]:
                print(f"   📰 {article['title'][:50]}...")
        else:
            print(f"❌ NewsAPI failed: {response.status_code}")
    except Exception as e:
        print(f"❌ NewsAPI error: {e}")
    
    print("\n🎯 Test complete!")

if __name__ == "__main__":
    test_api_endpoints()
