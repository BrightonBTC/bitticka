import requests

API_URL = 'https://explorer.brightbit.duckdns.org'

def fetch_from_api(url=API_URL, endpoint='/api/price'):
    if not url:
        return {'error':'Invalid URL'}

    try:
        response = requests.get(
            '{}{}'.format(url, endpoint), 
            headers={'User-Agent': 'LabDash HomeLab Dashboard'}
        )
        return response.json()
    
    except requests.RequestException as e:
        return {'error':'Something went wrong'}
	
