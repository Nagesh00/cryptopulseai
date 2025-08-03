# CryptoPulse AI - Quick Start Guide

## ✅ What's Working Now

Your CryptoPulse AI application is successfully running at: **http://127.0.0.1:5000**

### Current Status:
- ✅ Flask server running on port 5000
- ✅ Bootstrap UI with dark theme
- ✅ Project structure complete
- ✅ Background scheduler active
- ✅ Market data API endpoints ready
- ⚠️ API keys need configuration (expected errors shown in console)

## 🔧 Next Steps

### 1. Configure API Keys (Optional for testing)

Edit `config.py` with your actual API keys:

```python
# Get these free API keys:
NEWS_API_KEY = "your_newsapi_key_here"     # From newsapi.org
AI_API_KEY = "your_openai_key_here"        # From platform.openai.com  
PEXELS_API_KEY = "your_pexels_key_here"    # From pexels.com/api
```

### 2. Test the Application

Visit these URLs:

- **Homepage**: http://127.0.0.1:5000
- **Market Data API**: http://127.0.0.1:5000/api/market-data
- **Bitcoin Chart**: http://127.0.0.1:5000/coin/BTC
- **Ethereum Chart**: http://127.0.0.1:5000/coin/ETH

### 3. Features to Test

1. **Real-time Market Data**: The homepage table updates every 30 seconds
2. **Interactive Charts**: Click any coin in the table to view its chart
3. **Responsive Design**: Resize browser window to test mobile layout
4. **Navigation**: Use the navbar to navigate between sections

## 🛠️ Development Tips

### To Stop the Server:
Press `Ctrl+C` in the terminal

### To Restart After Changes:
```bash
C:/Users/Nagnath/crypto-pulse-ai/.venv/Scripts/python.exe app.py
```

### To Add New Features:
- Backend routes: Edit `app.py`
- Frontend styling: Edit `static/css/style.css`
- JavaScript: Edit `static/js/main.js` or `static/js/chart.js`
- Templates: Edit files in `templates/` folder

## 📊 Expected Behavior

### With API Keys:
- News articles will appear in the news section
- AI-generated articles will update daily
- Images will be fetched from Pexels

### Without API Keys (Current):
- Market data works (Binance API is free)
- Charts work (Binance API is free)
- News section shows placeholder
- Featured article shows default content
- Console shows API errors (this is normal)

## 🚀 Production Deployment

For production:
1. Use environment variables for API keys
2. Use a production WSGI server (e.g., Gunicorn)
3. Add caching for better performance
4. Implement rate limiting
5. Add error logging

## 📁 File Structure Recap

```
crypto-pulse-ai/
├── app.py              # ✅ Main Flask application  
├── config.py           # ⚠️ Add your API keys here
├── data.json           # ✅ Auto-generated data storage
├── requirements.txt    # ✅ Dependencies installed
├── templates/          # ✅ HTML templates
│   ├── layout.html     # ✅ Base layout
│   ├── index.html      # ✅ Homepage
│   └── coin_detail.html # ✅ Chart page
└── static/             # ✅ CSS & JavaScript
    ├── css/style.css   # ✅ Custom styles
    └── js/
        ├── main.js     # ✅ Homepage functionality  
        └── chart.js    # ✅ Chart functionality
```

Your CryptoPulse AI is ready to use! 🎉
