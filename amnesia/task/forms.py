from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.utils.translation import ugettext_lazy as _
from task.models import Task

from material import *

class CreateTaskForm(forms.ModelForm):
	
	def save(self, commit=True, *args, **kwargs):
		task = super(CreateTaskForm, self).save(commit=False)
		user = kwargs.pop('user')
		task.user = user
		if commit:
			try:
				task.save()
			except (IntegrityError, ValidationError):
				raise forms.ValidationError(_('Error Occurred while creating task'))
		return task
	
	class Meta:
		model = Task
		fields = ['message', 'every', 'sleep_cycle',]
