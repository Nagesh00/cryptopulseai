import requests

try:
    response = requests.get('http://127.0.0.1:5000/api/market-data')
    print('✅ Status Code:', response.status_code)
    
    data = response.json()
    print('✅ Number of items:', len(data))
    
    if data:
        print('✅ First item keys:', list(data[0].keys()))
        print('✅ First item symbol:', data[0]['symbol'])
        print('✅ Symbol ends with USDT:', data[0]['symbol'].endswith('USDT'))
        print('✅ Sample data:', data[0])
        
        # Test filtering
        usdt_items = [item for item in data if item['symbol'].endswith('USDT')]
        print('✅ USDT items after filtering:', len(usdt_items))
        
except Exception as e:
    print('❌ Error:', e)
