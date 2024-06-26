import requests
import config

def fetch_from_explorer(endpoint='/api/price'):
    
    try:
        response = requests.get(
            '{}{}'.format(config.EXPLORER_API_URL, endpoint), 
            headers={'User-Agent': 'Biticka Bitcoin Ticker'}
        )
        return response.json()
    
    except requests.RequestException as e:
        return {'error':'Something went wrong'}
	
