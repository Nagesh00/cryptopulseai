#!/usr/bin/env python3
"""
CryptoPulse AI - Startup Debug Test
Tests the startup functions that might be causing issues
"""

print("🚀 Testing CryptoPulse AI startup functions...")

try:
    # Import the main app components
    from app import fetch_latest_news, generate_daily_article, read_data, write_data
    print("✅ App functions imported successfully")
    
    # Test reading current data
    print("\n📄 Testing data file operations...")
    current_data = read_data()
    print(f"✅ Data read: {len(current_data.get('news_articles', []))} news articles")
    print(f"✅ Featured article: {'Yes' if current_data.get('featured_article') else 'No'}")
    
    # Test news fetching (this might timeout)
    print("\n📰 Testing news fetch (with timeout protection)...")
    try:
        fetch_latest_news()
        print("✅ News fetch completed successfully")
    except Exception as e:
        print(f"⚠️ News fetch failed: {e}")
    
    # Test article generation (this might timeout)
    print("\n🤖 Testing AI article generation (with timeout protection)...")
    try:
        generate_daily_article()
        print("✅ AI article generation completed")
    except Exception as e:
        print(f"⚠️ AI article generation failed: {e}")
    
    print("\n✅ Startup test completed - Flask app should be able to start now!")
    
except Exception as e:
    print(f"❌ Critical error: {e}")
    import traceback
    traceback.print_exc()
