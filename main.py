from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search=FlightSearch()
notification_manager = NotificationManager()

ORIGIN_CITY_IATA = "JAX"

# Check if iata code is missing in first city, if yes get the code and update the sheet
if sheet_data[0]["iataCode"] == "Testing":
    for row in sheet_data:
        row["iataCode"] = flight_search.get_iata_code(row["city"])
    data_manager.destination_data = sheet_data
    data_manager.update_iata_code()
   
tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))
    
for destination in sheet_data:
    flight = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"], 
        from_time=tomorrow,
        to_time=six_month_from_today
    )

if flight.price < destination["lowestPrice"]:
    notification_manager.send_sms(
        message=f"Low price alert! Only £{flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}."
        )