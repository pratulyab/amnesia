''' Script to send sms using TWILIO's library '''

import os, sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "amnesia.settings")
import django
django.setup()

from django.conf import settings
from twilio.rest import Client

def send_sms(message, to):
	client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
	message = client.messages.create(
	    to = to,
    	from_ = settings.MY_TWILIO_NUMBER,
	    body = message
	)
	return message.sid

def lookup_number(phone_number, country_code=''):
	''' Returns validity of number according to country code if provided '''
	client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
	number = None
	try:
		if country_code:
			number = client.lookups.phone_numbers(phone_number).fetch(type="carrier", country_code=country_code)
		else:
			number = client.lookups.phone_numbers(phone_number).fetch(type="carrier")
	except:
		return False
	return bool(number)

def get_message_status(msid):
	client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
	message = client.messages(msid).fetch()
	return {'status': message.status, 'body': message.body, 'error_code': message.error_code}
