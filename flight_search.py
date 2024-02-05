import os
import requests
import datetime
from dateutil.relativedelta import relativedelta
import dotenv

dotenv.load_dotenv()
IATA_ENDPOINT = "https://api.tequila.kiwi.com/locations/query"
SEARCH_ENDPOINT = "https://api.tequila.kiwi.com/v2/search"


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    FLY_FROM = 'POZ'

    def __init__(self) -> None:
        self.API_KEY = os.environ['KIWI_API_KEY']
        self.headers = {
            'accept': 'application/json',
            'apikey': self.API_KEY
        }

    # Return IATA code for city's airport.
    def search_airport(self, city: str) -> str:
        self.params = {
            'term': city,
            'locale': 'en-US',
            'location_types': 'airport',
            'limit': 1,
            'active_only': True
        }
        response = requests.get(IATA_ENDPOINT, headers=self.headers, 
                                params=self.params)
        response.raise_for_status()
        return response.json()['locations'][0]['code']

    # Check flight price for city
    def check_flight(self, city_iata: str) -> any:
        in_six_months = datetime.datetime.today() + relativedelta(months=+6)
        query = {
            'fly_from': self.FLY_FROM,
            'fly_to': city_iata,
            'date_from': datetime.datetime.today().strftime(r'%d/%m/%Y'),
            'date_to': in_six_months.strftime(r'%d/%m/%Y'),
            'curr': 'PLN',
            'limit': 1
        }
        response = requests.get(SEARCH_ENDPOINT, headers=self.headers, params=query)
        response.raise_for_status()
        return response.json()
