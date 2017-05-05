from celery.decorators import task
from celery.utils.log import get_task_logger

from account.models import CustomUser

from datetime import datetime
from sms import send_sms, get_message_status

from amnesia.celery import app

logger = get_task_logger(__name__)

MAX_RETRIES = 5 # Not setting Task.MaxRetries and handling Task.after_return because the error will be caused by the Twilio's API
# So, the message's status would indicate the success. Hence, it is better to do it this way.
# Also, by default celery has MAX_RETRIES set to 3, per task.

@app.task(name="send_sms_task")
def send_sms_task(message, user_pk, user_task_no):
	user = CustomUser.objects.select_related('phone_number').get(pk=user_pk)
	delivered = True
	number = user.phone_number.country.calling_code + user.phone_number.number
	for i in range(MAX_RETRIES):
		try:
			msid = send_sms(message, number)
			delivery_report = get_message_status(msid)
			if delivery_report['status'] in ['undelivered', 'failed'] or delivery_report['error_code']:
				delivered = False
				continue
			delivered = True
			break
		except:
			delivered = False
	
	log_message = "SUCCESS: %s: %s: Cronjob %d: Message \"%s\" sent to %s." if delivered else "FAILURE: %s: %s: Cronjob %d: Could not send message \" %s \" to %s"
	log_message = log_message % (datetime.now(), user.username, user_task_no, message, number)
	logger.info(log_message)
	user.logs += (log_message + '\n')
	user.save()
