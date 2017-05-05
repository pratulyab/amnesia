from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.core import validators
from django.db.utils import IntegrityError
from django.utils.translation import ugettext_lazy as _

from number.models import PhoneNumber
from sms import lookup_number

from material import *

class PhoneNumberForm(forms.ModelForm):
	calling_code = forms.CharField(label=_('Calling Code'), widget=forms.TextInput(attrs={'maxlength': 4}))

	def __init__(self, *args, **kwargs):
		super(PhoneNumberForm, self).__init__(*args, **kwargs)
		self.fields['number'].validators = [validators.RegexValidator(r'^\d{10}$')]
	
	def clean(self, *args, **kwargs):
		super(PhoneNumberForm, self).clean(*args, **kwargs)
		if self.cleaned_data.get('number', ''):
			phone_number = self.cleaned_data.get('calling_code', '') + self.cleaned_data['number']
			if not lookup_number(phone_number, self.cleaned_data['country'].code):
				raise forms.ValidationError(_('Not a valid number according to Twilio\'s Lookup API'))
		return self.cleaned_data

	def save(self, commit=True, *args, **kwargs):
		obj = super(PhoneNumberForm, self).save(commit=False, *args, **kwargs)
		if not self.cleaned_data.get('calling_code', '') or kwargs.get('calling_code', ''):
			raise forms.ValidationError(_('Calling code is required.'))
		if not obj.country.calling_code:
			obj.country.calling_code = self.cleaned_data['calling_code'] if self.cleaned_data.get('calling_code', '') else kwargs['calling_code']
		if commit:
			try:
				obj.save()
			except (ValidationError, IntegrityError):
				raise forms.ValidationError(_('Error Occurred. User with this number has already registered.'))
		return obj
	
	class Meta:
		model = PhoneNumber
		fields = ['country', 'number']
		help_texts = {
			'number': 'Make sure to enter a valid 10 digit number. It will be verified using Twilio\'s Lookup API',
		}
