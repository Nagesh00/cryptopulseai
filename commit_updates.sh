#!/bin/bash
# Commit script for CryptoPulse AI updates

echo "Committing CryptoPulse AI debug fixes..."

git add .
git commit -m "Fix CryptoPulse AI debug and error handling

- Added comprehensive debugging tools and error recovery
- Fixed startup sequence with graceful API timeout handling  
- Created app_minimal.py as reliable fallback version
- All APIs tested: CoinGecko, NewsAPI, Gemini AI working
- Ready for production deployment"

git push origin master

echo "✅ CryptoPulse AI updates pushed to GitHub!"
