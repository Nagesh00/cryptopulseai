# Deployment Guide for CryptoPulse AI

This guide covers various deployment options for the CryptoPulse AI cryptocurrency dashboard.

## Prerequisites

Before deploying, ensure you have:
1. Set up your API keys in `config.py` (copy from `config_template.py`)
2. Tested the application locally
3. All dependencies listed in `requirements.txt`

## 🚀 Deployment Options

### 1. Heroku Deployment (Recommended)

#### Step 1: Install Heroku CLI
Download and install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)

#### Step 2: Create Heroku App
```bash
# Login to Heroku
heroku login

# Create a new app
heroku create your-cryptopulse-app

# Set environment variables (replace with your actual keys)
heroku config:set NEWS_API_KEY="your_newsapi_key"
heroku config:set AI_API_KEY="your_gemini_key"
heroku config:set PEXELS_API_KEY="your_pexels_key"
```

#### Step 3: Create Procfile
Create a file named `Procfile` (no extension) in your project root:
```
web: python app.py
```

#### Step 4: Update app.py for Heroku
Add this to the bottom of your `app.py`:
```python
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

#### Step 5: Deploy
```bash
git add .
git commit -m "Prepare for Heroku deployment"
git push heroku master
```

### 2. Vercel Deployment

#### Step 1: Install Vercel CLI
```bash
npm install -g vercel
```

#### Step 2: Create vercel.json
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/app.py"
    }
  ]
}
```

#### Step 3: Deploy
```bash
vercel
```

Follow the prompts and add your environment variables in the Vercel dashboard.

### 3. Railway Deployment

#### Step 1: Connect GitHub
1. Go to [Railway.app](https://railway.app)
2. Connect your GitHub account
3. Select your repository

#### Step 2: Configure Environment Variables
Add your API keys in the Railway dashboard:
- `NEWS_API_KEY`
- `AI_API_KEY`
- `PEXELS_API_KEY`

#### Step 3: Deploy
Railway will automatically deploy from your GitHub repository.

### 4. DigitalOcean App Platform

#### Step 1: Create App
1. Go to [DigitalOcean](https://cloud.digitalocean.com/apps)
2. Create a new app from GitHub
3. Select your repository

#### Step 2: Configure
- Runtime: Python 3.13
- Build Command: `pip install -r requirements.txt`
- Run Command: `python app.py`

#### Step 3: Environment Variables
Add your API keys in the app settings.

### 5. PythonAnywhere

#### Step 1: Upload Files
Upload your project files to PythonAnywhere.

#### Step 2: Create Web App
1. Go to Web tab
2. Create new web app
3. Choose Flask framework

#### Step 3: Configure WSGI
Edit the WSGI configuration file to point to your app.py.

## 🔧 Environment Variables

For production deployment, set these environment variables instead of using `config.py`:

```bash
# News API
NEWS_API_KEY="your_newsapi_key_here"

# AI API (Google Gemini)
AI_API_KEY="your_gemini_api_key_here"

# Image API
PEXELS_API_KEY="your_pexels_api_key_here"
```

## 📝 Production Configuration

### Update app.py for Production
```python
import os

# Use environment variables in production
NEWS_API_KEY = os.environ.get('NEWS_API_KEY', 'fallback_key')
AI_API_KEY = os.environ.get('AI_API_KEY', 'fallback_key')
PEXELS_API_KEY = os.environ.get('PEXELS_API_KEY', 'fallback_key')
```

### Security Considerations
1. Never commit API keys to GitHub
2. Use environment variables for sensitive data
3. Enable HTTPS in production
4. Set up proper error logging
5. Configure rate limiting if needed

## 🔍 Troubleshooting

### Common Issues

1. **Port Issues**: Make sure your app listens on the correct port
2. **API Rate Limits**: Monitor your API usage
3. **Memory Limits**: Some platforms have memory restrictions
4. **Timeout Issues**: Configure appropriate timeouts for API calls

### Logs
Check platform-specific logs:
- Heroku: `heroku logs --tail`
- Vercel: Check function logs in dashboard
- Railway: View logs in project dashboard

## 🚀 Performance Optimization

1. **Caching**: Implement Redis for caching API responses
2. **Database**: Consider PostgreSQL for persistent data
3. **CDN**: Use CDN for static assets
4. **Background Jobs**: Use Celery for heavy tasks

## 📊 Monitoring

Set up monitoring for:
- API response times
- Error rates
- Memory usage
- User traffic

Popular monitoring tools:
- Sentry for error tracking
- New Relic for performance
- Datadog for infrastructure

---

**Choose the deployment option that best fits your needs and budget!**
