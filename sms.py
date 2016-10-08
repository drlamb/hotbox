# sms.py - Handles the Twilio messaging capabilities.

import logging
import configparser
import gps
from twilio.rest import TwilioRestClient
from twilio import TwilioRestException

config = configparser.ConfigParser()
config.read('config')
config = config['twilio']

client = TwilioRestClient(config['account_sid'], config['auth_token'])

print(config['auth_token'])

def send_text(message, temperature, delta, minutes_elapsed,
              number="+15163064504"):
    """
    Sends a text message to the specified number with temperature,
    minutes elapsed.

    TODO: multi phone number support, error checking, set origin number
    """
    message += " The inside of the car is currently %d° hot, with " \
               "a %d° change in %d minutes." % (temperature,
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
    pass
    
