# sms.py - Handles the Twilio messaging capabilities.

import logging
import ConfigParser
import mygps
from twilio.rest import TwilioRestClient
from twilio import TwilioRestException

config = ConfigParser.ConfigParser()
config.read('config')

client = TwilioRestClient(config.get('twilio', 'account_sid'), config.get('twilio', 'auth_token'))

# The function that uses twilio to send the car's owner a SMS
def send_text(message, temperature, delta, minutes_elapsed,
              number="+17348463494"):
    """
    Sends a text message to the specified number with temperature,
    minutes elapsed.
    """
    message += " The inside of the car is currently %d degrees, with " \
               "a %d degree change in %d minutes." % (temperature,
                                                delta, minutes_elapsed)
    try:
        sms = client.messages.create(body=message,
                                     to=number,
                                     from_=config.get('twilio', 'from_number'))
    except TwilioRestException as e:
        print(repr(e))
        logging.error(repr(e))

def contact_911():
    """
    If too much time has elapsed without any detected change in the
    car, or if it becomes far too hot too quickly, get the nearest 
    authorities. This section left unfilled due to variences in support between
    police departments.
    """
    (lat, lon) = mygps.get_coords()
    print lat
    print lon
    
    
