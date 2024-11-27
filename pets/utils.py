""" Utils page for Twilio API """
from twilio.rest import Client
from django.conf import settings

def send_sms(to, message):
    """ Function to send message to whatsapp """
    # Create a Twilio client
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    # Send SMS
    client.messages.create(
        body=message,
        from_=settings.TWILIO_PHONE_NUMBER,
        to=to
    )
