#!/usr/bin/env python3
"""
CryptoPulse AI - Complete Debug Script
Tests all components of your crypto dashboard
"""

import requests
import json
import sys
from datetime import datetime

def test_binance_api():
    """Test Binance API connection"""
    print("🔍 Testing Binance API...")
    try:
        # Test single coin
        response = requests.get("https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Binance API working - BTC: ${float(data['lastPrice']):,.2f} ({data['priceChangePercent']}%)")
            return True
        else:
            print(f"❌ Binance API error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Binance API connection failed: {e}")
        return False

def test_coingecko_api():
    """Test CoinGecko API connection"""
    print("🔍 Testing CoinGecko API...")
    try:
        response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ CoinGecko API working - BTC: ${data['bitcoin']['usd']:,.2f}, ETH: ${data['ethereum']['usd']:,.2f}")
            return True
        else:
            print(f"❌ CoinGecko API error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ CoinGecko API connection failed: {e}")
        return False

def test_news_api():
    """Test NewsAPI connection"""
    print("🔍 Testing NewsAPI...")
    try:
        from config import NEWS_API_KEY
        params = {
            'apiKey': NEWS_API_KEY,
            'category': 'business',
            'language': 'en',
            'pageSize': 5
        }
        response = requests.get("https://newsapi.org/v2/top-headlines", params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            print(f"✅ NewsAPI working - Found {len(articles)} articles")
            if articles:
                print(f"   Latest: {articles[0]['title'][:60]}...")
            return True
        else:
            print(f"❌ NewsAPI error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ NewsAPI connection failed: {e}")
        return False

def test_gemini_api():
    """Test Google Gemini AI API"""
    print("🔍 Testing Gemini AI API...")
    try:
        from config import AI_API_KEY
        test_prompt = "Write a brief 50-word summary about Bitcoin."
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": test_prompt
                }]
            }]
        }
        
        response = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={AI_API_KEY}",
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            content = data['candidates'][0]['content']['parts'][0]['text']
            print(f"✅ Gemini AI working - Generated: {content[:60]}...")
            return True
        else:
            print(f"❌ Gemini AI error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Gemini AI connection failed: {e}")
        return False

def test_pexels_api():
    """Test Pexels API connection"""
    print("🔍 Testing Pexels API...")
    try:
        from config import PEXELS_API_KEY
        headers = {'Authorization': PEXELS_API_KEY}
        params = {'query': 'cryptocurrency', 'per_page': 1}
        
        response = requests.get("https://api.pexels.com/v1/search", headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            photos = data.get('photos', [])
            print(f"✅ Pexels API working - Found {len(photos)} images")
            if photos:
                print(f"   Image URL: {photos[0]['src']['medium']}")
            return True
        else:
            print(f"❌ Pexels API error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Pexels API connection failed: {e}")
        return False

def test_flask_imports():
    """Test Flask and other imports"""
    print("🔍 Testing Python imports...")
    try:
        import flask
        import requests
        import json
        from apscheduler.schedulers.background import BackgroundScheduler
        from datetime import datetime
        print("✅ All required imports working")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_data_file():
    """Test data.json file operations"""
    print("🔍 Testing data file operations...")
    try:
        # Test data file creation/reading
        test_data = {
            "featured_article": {
                "title": "Test Article",
                "summary": "Test summary",
                "content": "Test content",
                "image_url": "https://via.placeholder.com/300"
            },
            "news_articles": [
                {
                    "source": "Test Source",
                    "title": "Test News",
                    "url": "https://example.com",
                    "image_url": "https://via.placeholder.com/150",
                    "published_at": datetime.now().isoformat()
                }
            ]
        }
        
        # Write test data
        with open('data.json', 'w') as f:
            json.dump(test_data, f, indent=2)
        
        # Read test data
        with open('data.json', 'r') as f:
            loaded_data = json.load(f)
        
        print("✅ Data file operations working")
        return True
    except Exception as e:
        print(f"❌ Data file error: {e}")
        return False

def run_full_debug():
    """Run complete debug suite"""
    print("🚀 CryptoPulse AI - Complete Debug Report")
    print("=" * 50)
    print(f"Debug started at: {datetime.now()}")
    print()
    
    tests = [
        ("Flask Imports", test_flask_imports),
        ("Data File Operations", test_data_file),
        ("Binance API", test_binance_api),
        ("CoinGecko API", test_coingecko_api),
        ("NewsAPI", test_news_api),
        ("Gemini AI", test_gemini_api),
        ("Pexels API", test_pexels_api),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results[test_name] = False
        print()
    
    print("📊 Debug Summary:")
    print("=" * 30)
    total_tests = len(results)
    passed_tests = sum(results.values())
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\nOverall: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All systems operational! Your CryptoPulse AI is ready to launch!")
    else:
        print("⚠️  Some issues detected. Review the failed tests above.")
    
    return results

if __name__ == "__main__":
    run_full_debug()
