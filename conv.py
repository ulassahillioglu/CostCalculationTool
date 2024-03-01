import requests as rq
from bs4 import BeautifulSoup as bs

def currency_converter():
    url = "https://www.x-rates.com/calculator/?from=USD&to=TRY&amount=1"
    response = rq.get(url)
    soup = bs(response.text, 'html.parser')
    result = soup.find('span', {'class': 'ccOutputRslt'}).text
    result = round(float(result.strip('TRY').strip()),2)
    
    return result

