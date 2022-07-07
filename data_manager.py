from pprint import pprint
import requests
from keys import  SHEET_USERNAME, SHEET_PROJECT, SHEET2_SHEETNAME, BEARER

sheety_prices_endpoint ="https://api.sheety.co/{SHEET_USERNAME}/{SHEET_PROJECT}/{SHEET_SHEETNAME}"
bearer_headers = {
    "Authorization": BEARER
}
class DataManager:
    
    def __init__(self):
        self.destination_data={}

    def get_destination_data(self):
        response = requests.get(url="https://api.sheety.co/609181b74b070263b23fcc3b0bb6bb5a/flightFinder/prices")
        data = response.json()
        self.destination_data= data["prices"]
        return self.destination_data

    def update_destination_code(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(f'{sheety_prices_endpoint}/{city["id"]}', json=new_data, headers=bearer_headers)
            print(response.text)
            
            
    def get_customer_emails(self):
        customers_endpoint =f"https://api.sheety.co/{SHEET_USERNAME}/{SHEET_PROJECT}/{SHEET2_SHEETNAME}"
        response = requests.get(url=customers_endpoint, headers=bearer_headers)
        data = response.json()
        self.customer_data = data["users"]