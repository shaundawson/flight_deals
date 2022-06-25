import gzip
import requests
from flight_data import FlightData
from keys import TEQUILA_API_KEY, TEQUILA_SEARCH_API_KEY


TEQUILA_KIWI_ENDPOINT = "https://tequila-api.kiwi.com"

HEADERS = {
    "apikey": TEQUILA_API_KEY,
    "Content-Type": "application/json",
    }

HEADERS_SEARCH = {
    "apikey": TEQUILA_SEARCH_API_KEY,
    "Content-Type": "application/json",
    }

class FlightSearch:
    def get_iata_code(self, city):
        global HEADERS
        search_params = {
            "term": city,
            "location-types": "city",
        }
        response = requests.get(url=f"{TEQUILA_KIWI_ENDPOINT}/locations/query",headers=HEADERS,params=search_params)
        results = response.json()["locations"]
        code = results[0]["code"]
        return code


    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        global HEADERS_SEARCH
        flight_search_params = {
            "fly_from": origin_city_code, 
            "fly_to": destination_city_code ,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 1,
            "curr": "USD"
        }
        response = requests.get(f"{TEQUILA_KIWI_ENDPOINT}/v2/search",params=flight_search_params, headers=HEADERS_SEARCH) 
        try:
           data = response.json()["data"]
        except IndexError:
            print(f"No flight found for {destination_city_code}.")
            return None
        
        flight_data = FlightData(
            price=data[0]["price"],
            origin_city=data[0]["route"][0]["cityFrom"],
            origin_airport=data[0]["route"][0]["flyFrom"],
            destination_city=data[0]["route"][0]["cityTo"],
            destination_airport=data[0]["route"][0]["flyTo"],
            out_date=data[0]["route"][0]["local_departure"].split("T")[0],
            return_date=data[0]["route"][1]["local_departure"].split("T")[0]
        )

        print(f"{flight_data.destination_city}: £{flight_data.price}")
        return flight_data
        
        