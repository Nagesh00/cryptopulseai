import requests

def test_coingecko_api():
    """Test if CoinGecko API is working"""
    try:
        # Test basic connectivity
        response = requests.get('https://api.coingecko.com/api/v3/ping', timeout=10)
        print('CoinGecko ping status:', response.status_code)
        
        # Test market data
        response = requests.get(
            'https://api.coingecko.com/api/v3/coins/markets',
            params={
                'vs_currency': 'usd',
                'order': 'market_cap_desc',
                'per_page': 10,
                'page': 1,
                'sparkline': False,
                'price_change_percentage': '24h'
            },
            timeout=10
        )
        print('CoinGecko market data status:', response.status_code)
        
        if response.status_code == 200:
            data = response.json()
            print(f'Sample data: {len(data)} coins received')
            if data:
                coin = data[0]
                print(f'Bitcoin price: ${coin["current_price"]}')
                print(f'24h change: {coin.get("price_change_percentage_24h", 0):.2f}%')
                return True
        
    except Exception as e:
        print(f'Error: {e}')
        return False

if __name__ == "__main__":
    test_coingecko_api()
