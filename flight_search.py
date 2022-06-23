import requests
from keys import SHEET_USERNAME, SHEET_PROJECT, SHEET_SHEETNAME, BEARER
  
SHEET_HEADERS = {
    'Authorization': BEARER
}
class FlightSearch:
    sheet_endpoint = f'https://api.sheety.co/{SHEET_USERNAME}/{SHEET_PROJECT}/{SHEET_SHEETNAME}'
    sheet_response = requests.get(url=sheet_endpoint, headers=SHEET_HEADERS)
    result = sheet_response.json()
    # print(result)