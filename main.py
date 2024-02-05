# This file will need to use the DataManager,FlightSearch, FlightData,
# NotificationManager classes to achieve the program requirements.
import data_manager
import flight_search

fs = flight_search.FlightSearch()
fs.check_flight('CDG')
