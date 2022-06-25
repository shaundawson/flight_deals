from pprint import pprint
import requests
from keys import  SHEET_USERNAME, SHEET_PROJECT, SHEET_SHEETNAME, BEARER


sheety_endpoint = f'https://api.sheety.co/{SHEET_USERNAME}/{SHEET_PROJECT}/{SHEET_SHEETNAME}'

bearer_headers = {
    "Authorization": BEARER
}
class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self ):
        self.destination_data = {}

    def get_destination_data(self):
        sheet_response = requests.get(sheety_endpoint, headers=bearer_headers)
        data = sheet_response.json()
        print(data)
        self.destination_data = data["prices"]
        return self.destination_data

    def update_iata_code(self):
        for city in self.destination_data:
            new_data = {
                "prices": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(f"{sheety_endpoint}/{city['id']}", json=new_data, headers=bearer_headers)
            print(response.text)