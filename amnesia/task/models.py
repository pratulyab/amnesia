from django.db import models
from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule

from account.models import CustomUser

import json

# Create your models here.

# Storing the complementary time cycle in DB
SLEEP_CYCLES = (
		('*', 'None. Send every hour.'),
		('4-19', '8pm - 4am'),
		('5-20', '9pm - 5am'),
		('6-21', '10pm - 6am'),
		('7-22', '11pm - 7am'),
		('8-23', '12am - 8am'),
	)

# 60 minutes = 1 hour, therefore 0 min; i.e. execute at the hour
# Default is 1 60 minutes
REPEAT_CYCLES = (
		('*', 'every minute'),
		('*/15', '15 minutes'),
		('*/30', '30 minutes'),
		('0', '60 minutes (hour)'),
	)

class Task(models.Model):
	celery_task = models.ForeignKey(PeriodicTask, related_name="user_tasks", blank=True)
	user = models.ForeignKey(CustomUser, related_name="tasks")
	message = models.CharField(max_length=160)
	sleep_cycle = models.CharField(max_length=5, choices=SLEEP_CYCLES, default=SLEEP_CYCLES[1][0], help_text="Assuming 8 hours sleep cycle. No messages will be sent during sleep cycle.")
	every = models.CharField(max_length=4, choices=REPEAT_CYCLES, default=REPEAT_CYCLES[3][0], help_text="Repeat every")
	created_on = models.DateTimeField(auto_now_add=True)

	def save(self, *args, **kwargs):
		crontab, created = CrontabSchedule.objects.get_or_create(
			minute = self.every,
			hour = self.sleep_cycle,
			day_of_week = '*',
			day_of_month = '*',
			month_of_year = '*'
		)
		
		periodic_task = PeriodicTask.objects.create(
			crontab = crontab,
			name = self.user.username + str(self.user.total_tasks_created), # since username is unique & total tasks increment
			task = 'send_sms_task',
			args = json.dumps([self.message, self.user.pk, self.user.total_tasks_created]),
		)

		self.celery_task = periodic_task
		super(Task, self).save()
		self.user.total_tasks_created += 1
		self.user.save()
