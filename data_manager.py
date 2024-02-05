import os
import requests
import dotenv
import flight_search as fs

dotenv.load_dotenv()
ENDPOINT = "https://api.sheety.co/ea3c009c05b356f18facfc9feeecbbff/flightDeals/prices"


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self) -> None:
        self.API_KEY = os.environ['SHEETY_AUTH']
        self.header = {
            'Authorization': self.API_KEY,
            'Content-Type': 'application/json'
            }

    # Sets IATA codes in the spreadsheet
    def update_IATA_codes(self) -> None:
        get_cities = requests.get(ENDPOINT, headers=self.header)
        get_cities.raise_for_status()
        get_cities = get_cities.json()
        search = fs.FlightSearch()

        for row in get_cities['prices']:
            if not row['iataCode']:
                iata = search.search_airport(row['city'])

                data = {
                    'price': {
                        'city': row['city'],
                        'iataCode': iata,
                        'lowestPrice': row['lowestPrice']
                    }
                }
                send_code = requests.put(url=(ENDPOINT + f"/{row['id']}"),
                                         headers=self.header, json=data)
                send_code.raise_for_status

    # Get new prices and update them in the sheet
    def update_prices(self) -> None:
        # Get flight prices
        flight_prices = {}

        # Add prices for all flights to prices dict
        for row in get_prices['data']:
            prices[row['flyTo']] = row['price']

        get_sheet = requests.get(ENDPOINT, headers=self.header)