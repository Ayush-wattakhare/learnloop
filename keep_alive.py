"""
Keep-Alive Script for Render Free Tier
Pings the app every 10 minutes to prevent cold starts
"""
import requests
import time
import os

APP_URL = os.environ.get('APP_URL', 'https://learnloop-rkhq.onrender.com')
PING_INTERVAL = 600  # 10 minutes

def ping_app():
    try:
        response = requests.get(f'{APP_URL}/', timeout=10)
        print(f'✅ Ping successful: {response.status_code}')
        return True
    except Exception as e:
        print(f'❌ Ping failed: {str(e)}')
        return False

if __name__ == '__main__':
    print(f'🔄 Starting keep-alive for {APP_URL}')
    print(f'   Pinging every {PING_INTERVAL} seconds')
    
    while True:
        ping_app()
        time.sleep(PING_INTERVAL)
