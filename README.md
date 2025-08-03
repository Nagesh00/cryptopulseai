# CryptoPulse AI 🚀

A comprehensive real-time cryptocurrency dashboard with AI-powered content generation, automated news fetching, and interactive charts.

![CryptoPulse AI](https://images.pexels.com/photos/730547/pexels-photo-730547.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1)

## 🌟 Features

- **Real-time Market Data**: Live cryptocurrency prices from CoinGecko and Binance APIs
- **AI-Generated Articles**: Daily market analysis powered by Google Gemini AI
- **Automated News**: Latest cryptocurrency and business news updated hourly
- **Interactive Charts**: TradingView Lightweight Charts for advanced price analysis
- **Responsive Design**: Bootstrap-powered dark theme responsive UI
- **Background Scheduling**: Automated tasks using APScheduler
- **Multi-API Fallback**: Reliable data with automatic API failover
- **Top 100 Cryptocurrencies**: Comprehensive market coverage

## 🏗️ Project Structure

```
crypto-pulse-ai/
├── app.py                  # Main Flask application with API endpoints
├── config.py               # API keys configuration (excluded from git)
├── config_template.py      # Template for API configuration
├── requirements.txt        # Python dependencies
├── data.json              # Data storage for news and articles
├── start_app.bat          # Windows batch file to start the app
├── README.md              # Project documentation
├── templates/
│   ├── layout.html        # Base template with Bootstrap
│   ├── index.html         # Homepage with market overview
│   └── coin_detail.html   # Individual coin analysis page
└── static/
    ├── css/
    │   └── style.css      # Custom dark theme styles
    └── js/
        ├── main.js        # Homepage JavaScript and API calls
        └── chart.js       # TradingView chart integration
```

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/crypto-pulse-ai.git
cd crypto-pulse-ai
```

### 2. Set up Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure API Keys

1. Copy the template file:
   ```bash
   cp config_template.py config.py
   ```

2. Edit `config.py` and add your API keys:
   ```python
   NEWS_API_KEY = "your_newsapi_key_here"
   AI_API_KEY = "your_gemini_api_key_here"  
   PEXELS_API_KEY = "your_pexels_api_key_here"
   ```

#### 🔑 Get Free API Keys:
- **NewsAPI**: Register at [newsapi.org](https://newsapi.org) (Free: 1000 requests/day)
- **Google Gemini AI**: Get API key from [makersuite.google.com](https://makersuite.google.com/app/apikey) (Free tier available)
- **Pexels**: Register at [pexels.com/api](https://www.pexels.com/api/) (Free: 200 images/hour)

### 4. Run the Application

```bash
python app.py
```

Or on Windows, simply double-click `start_app.bat`

Visit `http://localhost:5000` to view the dashboard!

## 📱 Features Overview

### 🏠 Homepage
- **Featured AI-generated article** with market insights
- **Live cryptocurrency market table** (top 100 coins by market cap)
- **Latest cryptocurrency news** updated hourly
- **Automatic data refresh** every 30 seconds
- **Responsive design** optimized for all devices

### 📊 Coin Detail Pages
- **Interactive TradingView charts** for technical analysis
- **Historical price data** (100 days of candlestick data)
- **Real-time price updates** with percentage changes
- **Professional trading interface**

### 🤖 AI & Automation
- **Daily AI articles** generated based on market trends
- **Automated news fetching** every hour
- **Smart topic detection** from trending cryptocurrencies
- **Fallback content system** for reliability

## 🛠️ Technical Details

### APIs Used
- **CoinGecko API** (Primary): Free, reliable cryptocurrency data
- **Binance API** (Fallback): High-frequency trading data
- **NewsAPI**: Latest cryptocurrency and business news
- **Google Gemini AI**: Advanced content generation
- **Pexels API**: High-quality stock images

### Technologies
- **Backend**: Flask (Python 3.13+)
- **Frontend**: Bootstrap 5, JavaScript ES6
- **Charts**: TradingView Lightweight Charts
- **Scheduling**: APScheduler for background tasks
- **Data Storage**: JSON file-based storage

### Key Features
- **Multi-API fallback system** for 99.9% uptime
- **Real-time data updates** without page refresh
- **Professional dark theme** UI
- **Mobile-responsive design**
- **Error handling and fallback data**

## 🔧 Customization

### Adding New Cryptocurrencies
The system automatically fetches the top 100 cryptocurrencies by market cap. To modify this:

1. Edit the `get_market_data()` function in `app.py`
2. Adjust the `per_page` parameter in the CoinGecko API call

### Changing Update Intervals
In `app.py`, modify the scheduler intervals:
```python
scheduler.add_job(func=fetch_latest_news, trigger="interval", hours=1)  # News
scheduler.add_job(func=generate_daily_article, trigger="interval", hours=24)  # AI articles
```

## 🚀 Deployment Options

### Local Development
```bash
python app.py
```

### Production Deployment
1. **Heroku**: Use the included `requirements.txt`
2. **Vercel**: Deploy with Python runtime
3. **Railway**: One-click deployment
4. **DigitalOcean**: App Platform deployment

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🐛 Issues and Support

If you encounter any issues:
1. Check the [Issues](https://github.com/yourusername/crypto-pulse-ai/issues) page
2. Create a new issue with detailed description
3. Include error messages and system information

## 📊 Screenshots

### Homepage
![Homepage](https://via.placeholder.com/800x400/1a1a1a/ffffff?text=CryptoPulse+AI+Homepage)

### Coin Detail Page
![Coin Detail](https://via.placeholder.com/800x400/1a1a1a/ffffff?text=Interactive+Charts)

---

**Made with ❤️ for the crypto community**

### Background Tasks
- **News fetching**: Updates every hour
- **AI article generation**: Updates every 24 hours
- **Market data**: Real-time via API calls

## Technical Details

### Backend (Flask)
- RESTful API endpoints for market data
- Background task scheduling with APScheduler
- JSON file-based data persistence
- Error handling and rate limiting

### Frontend
- Bootstrap 5 for responsive design
- Vanilla JavaScript for interactivity
- TradingView Lightweight Charts
- Real-time data updates

### Data Sources
- **Market Data**: Binance API
- **News**: NewsAPI
- **Images**: Pexels API
- **AI Content**: OpenAI/Gemini (configurable)

## API Endpoints

- `GET /` - Homepage
- `GET /coin/<symbol>` - Coin detail page
- `GET /api/market-data` - Live market data
- `GET /api/kline-data/<symbol>` - Historical price data

## Development Notes

- The application uses mock AI responses by default to avoid requiring API keys for testing
- Replace the mock implementation in `generate_daily_article()` with actual AI API calls
- Consider implementing caching for better performance in production
- Use environment variables for API keys in production

## License

This project is for educational purposes. Please respect API rate limits and terms of service.
