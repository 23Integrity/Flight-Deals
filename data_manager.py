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

    # Returns a list of flights_to - as IATA codes
    def get_current_flight_prices(self) -> dict:
        iata_prices = {}
        get_cities = requests.get(ENDPOINT, headers=self.header)
        get_cities.raise_for_status()
        get_cities = get_cities.json()

        for row in get_cities['prices']:
            iata_prices[row['iataCode']] = row['lowestPrice']
        return iata_prices

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
    # Returns a tuple:
    #   - bool indicates the change,
    #   - dict is a dictionary of prices
    #   (doesn't matter if price changed)
    def update_prices(self) -> (bool, dict):
        get_flights = self.get_current_flight_prices()  # dict with lowest prices yet
        new_prices = {}  # dict with prices for today
        search = fs.FlightSearch()
        change = False

        # Search and save current prices
        for flight in get_flights:
            flight_status = search.check_flight(flight)
            new_prices[flight] = flight_status['data'][0]['price']

        # Compare prices
        for flight in get_flights:
            if get_flights[flight] > new_prices[flight]:
                get_flights[flight] = new_prices[flight]
                change = True
        return change, get_flights
    
    # Update my spreadsheet with new values
    def update_spreadsheet(self, prices: dict) -> None:

