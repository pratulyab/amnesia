from django.db import models
from django.contrib.auth.models import AbstractUser

from number.models import PhoneNumber

# Create your models here.

class CustomUser(AbstractUser):
	def __init__(self, *args, **kwargs):
		self._meta.get_field('first_name').blank = False # Making first name required
		super(CustomUser, self).__init__(*args, **kwargs)
	
	phone_number = models.OneToOneField(PhoneNumber)
	total_tasks_created = models.PositiveSmallIntegerField(default=0)
	logs = models.TextField(blank=True) # Creating a text field for logs instead of separate model for simplicity purposes

	def __str__(self):
		return self.first_name + self.last_name
