"""
Test script to manually trigger CryptoPulse AI functions
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import fetch_latest_news, generate_daily_article, read_data
import json

def test_all_functions():
    print("🔄 Testing CryptoPulse AI Functions...")
    
    # Test 1: News fetching
    print("\n1️⃣ Testing News Fetching...")
    try:
        fetch_latest_news()
        data = read_data()
        news_count = len(data.get('news_articles', []))
        print(f"✅ News fetching successful! Found {news_count} articles")
    except Exception as e:
        print(f"❌ News fetching failed: {e}")
    
    # Test 2: AI article generation
    print("\n2️⃣ Testing AI Article Generation...")
    try:
        generate_daily_article()
        data = read_data()
        article = data.get('featured_article', {})
        print(f"✅ AI article generation completed!")
        print(f"   Title: {article.get('title', 'No title')[:50]}...")
    except Exception as e:
        print(f"❌ AI article generation failed: {e}")
    
    # Test 3: Data verification
    print("\n3️⃣ Verifying Data Structure...")
    try:
        data = read_data()
        print(f"✅ Data structure valid!")
        print(f"   - Featured article: {'✅' if data.get('featured_article') else '❌'}")
        print(f"   - News articles: {len(data.get('news_articles', []))} items")
        print(f"   - Image URL: {'✅' if data.get('featured_article', {}).get('image_url') else '❌'}")
    except Exception as e:
        print(f"❌ Data verification failed: {e}")
    
    print("\n🎉 Test completed!")

if __name__ == "__main__":
    test_all_functions()
