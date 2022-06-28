import pprint
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
    
    def __init__(self):
        self.city_codes = []
        
    def get_iata_code(self, city_names):
        print("get destination codes triggered")
        global HEADERS
        for city in city_names:
            search_params = {
                "term": city_names,
                "location-types": "city",
            }
            response = requests.get(url=f"{TEQUILA_KIWI_ENDPOINT}/locations/query",headers=HEADERS,params=search_params)
            results = response.json()["locations"]
            code = results[0]["code"]
            self.city_codes.append(code)
            
            return self.city_codes


    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        print(f"Check flights triggered for {destination_city_code}")
        global HEADERS_SEARCH
        flight_search_params = {
            "fly_from": origin_city_code, 
            "fly_to": destination_city_code ,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 3,
            "nights_in_dst_to": 14,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 2,
            "curr": "USD"
        }
        response = requests.get(f"{TEQUILA_KIWI_ENDPOINT}/v2/search",params=flight_search_params, headers=HEADERS_SEARCH) 
        
        try:
           data = response.json()["data"][0]
           
        except IndexError:
            flight_search_params["max_stopovers"] = 1
            response = requests.get(f"{TEQUILA_KIWI_ENDPOINT}/v2/search",params=flight_search_params, headers=HEADERS_SEARCH) 
            data = response.json()["data"][0]
            pprint(data)
            flight_data = FlightData(
                price=data[0]["price"],
                origin_city=data[0]["route"][0]["cityFrom"],
                origin_airport=data[0]["route"][0]["flyFrom"],
                destination_city=data[0]["route"][0]["cityTo"],
                destination_airport=data[0]["route"][0]["flyTo"],
                out_date=data[0]["route"][0]["local_departure"].split("T")[0],
                return_date=data[0]["route"][1]["local_departure"].split("T")[0],
                stop_overs=1,
                via_city=data["route"][0]["cityTo"]
            )
            return flight_data
            
        else:
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][0]["cityTo"],
                destination_airport=data["route"][0]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0]
        )
            return flight_data
        
        