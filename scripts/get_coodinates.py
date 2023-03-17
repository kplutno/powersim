from unidecode import unidecode
from urllib.parse import quote
import requests

if __name__=="__main__":
    
    country = "Poland"
    state = "Mazowieckie"
    county = "Pruszkowski"
    
    url = f"https://nominatim.openstreetmap.org/?country={quote(country)}&state={quote(state)}&county={quote(county)}&format=json"
    
    response = requests.get(url).json()
    
    print(response[0].get("lat"))
    