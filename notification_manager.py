from twilio.rest import Client
import smtplib
from keys import TWILIO_AUTH_TOKEN, TWILIO_SID, TWILIO_VERIFIED_NUMBER, TWILIO_VIRTUAL_NUMBER, MY_EMAIL, PASSWORD

TWILIO_SID = TWILIO_SID
TWILIO_AUTH_TOKEN = TWILIO_AUTH_TOKEN
TWILIO_VIRTUAL_NUMBER = TWILIO_VIRTUAL_NUMBER
TWILIO_VERIFIED_NUMBER = TWILIO_VERIFIED_NUMBER
class NotificationManager:

    def __init__(self):
        self.client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    def send_sms(self, message):
        message = self.client.messages.create(
            body=message,
            from_=TWILIO_VIRTUAL_NUMBER,
            to=TWILIO_VERIFIED_NUMBER,
        )
        # Prints if successfully sent.
        print(message.sid)
        
    def send_emails(self, emails, message, google_flight_link):
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as connection:
            # connection.starttls()
            connection.ehlo()
            connection.login(user=MY_EMAIL, password=PASSWORD)
            for email in emails:
                connection.sendmail(
                    from_addr=MY_EMAIL, 
                    to_addrs=email["email"], 
                    msg=f"Subject:New Low Price Flight!\n\n{message}\n{google_flight_link}".encode('utf-8')
                )