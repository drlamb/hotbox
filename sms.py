# sms.py - Handles the Twilio messaging capabilities.

import logging
import ConfigParser
import mygps
from twilio.rest import TwilioRestClient
from twilio import TwilioRestException

config = ConfigParser.ConfigParser()
config.read('config')
#config = config.items('twilio')

client = TwilioRestClient(config.get('twilio', 'account_sid'), config.get('twilio', 'auth_token'))


def send_text(message, temperature, delta, minutes_elapsed,
              number="+15163064504"):
    """
    Sends a text message to the specified number with temperature,
    minutes elapsed.

    TODO: multi phone number support, error checking, set origin number
    """
    message += " The inside of the car is currently %d degrees hot, with " \
               "a %d degree change in %d minutes." % (temperature,
                                                delta, minutes_elapsed)
    try:
        sms = client.messages.create(body=message,
                                     to=number,
                                     from_=config['from_number'])
    except TwilioRestException as e:
        print(repr(e))
        logging.error(repr(e))

def contact_911():
    """
    If too much time has elapsed without any detected change in the
    car, or if it becomes far too hot too quickly, get the nearest 
    authorities.
    """
    (lat, lon) = mygps.get_coords()
    print lat
    print lon
    #pass
    
contact_911()
