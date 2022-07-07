from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

ORIGIN_CITY_IATA = "MCO"

data_manager = DataManager()
flight_search=FlightSearch()
notification_manager = NotificationManager()

sheet_data = data_manager.get_destination_data()

if sheet_data[0]["iataCode"] == "":
    for row in sheet_data:
        row["iataCode"] = flight_search.get_destination_code(row["city"])
    data_manager.destination_data = sheet_data
    data_manager.update_destination_code()

   
tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))
    
for destination_code in sheet_data:
    flight = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination_code["iataCode"], 
        from_time=tomorrow,
        to_time=six_month_from_today
    )
    
    print(flight.price)
    if flight is None:
        continue

    # users = data_manager.get_customer_emails()
    # emails = [row["email"] for row in users]
    # names = [row["firstName"] for row in users]
    # message = f"Low price alert! Only {flight.price}USD to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}."
    # if flight.stop_overs > 0:
    #         message += f"\n\nFlight has {flight.stop_overs}, via {flight.via_city}."
    # link = f"https://www.google.com/flights?hl=en#flt={flight.origin_airport}.{flight.destination_airport}.{flight.out_date}*{flight.destination_airport}.{flight.origin_airport}.{flight.return_date}"
    
    # notification_manager.send_emails(emails, message, link)
