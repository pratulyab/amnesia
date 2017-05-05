from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.utils.translation import ugettext_lazy as _
from account.models import CustomUser

import re
from material import *

class LoginForm(forms.Form):
	username = forms.CharField(label=_('Username'), widget=forms.TextInput(attrs={'placeholder': _('Enter username'), 'auto_focus':''}))
	password = forms.CharField(label=_('Password'), widget=forms.PasswordInput({'placeholder': _('Enter password')}))

	def __init__(self, *args, **kwargs):
		self.user_cache = None
		super(LoginForm, self).__init__(*args, **kwargs)

	def clean(self):
		super(LoginForm, self).clean()
		username = self.cleaned_data.get('username', None)
		password = self.cleaned_data.get('password', None)

		if username and password:
			try:
				CustomUser.objects.get(username=username)
			except CustomUser.DoesNotExist:
				raise forms.ValidationError(_('Invalid username'))
			self.user_cache = authenticate(username=username, password=password)
			if self.user_cache is None:
				raise forms.ValidationError(_('Invalid username or password'))
		return self.cleaned_data

	def get_user(self):
		return self.user_cache

class SignupForm(forms.ModelForm):
	password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput(attrs={'placeholder': _('Enter password')}))
	password2 = forms.CharField(label=_('Re-enter Password'), widget=forms.PasswordInput(attrs={'placeholder': _('Confirm password')}))

	def clean(self, *args, **kwargs):
		super(SignupForm, self).clean(*args, **kwargs)
		pwd1 = self.cleaned_data.get('password1', None)
		pwd2 = self.cleaned_data.get('password2', None)
		if pwd1 and pwd2:
			if pwd1 != pwd2:
				raise forms.ValidationError(_('Passwords do not match.'))
			password_validation.validate_password(pwd1)
		return self.cleaned_data

	def save(self, commit=True, *args, **kwargs):
		user = super(SignupForm, self).save(commit=False)
		user.set_password(self.cleaned_data.get('password2'))
		if commit:
			try:
				user.save()
			except IntegrityError:
				raise forms.ValidationError(_('User already exists'))
			except ValidationError as error:
				raise forms.ValidationError(error)
		return user

	class Meta:
		model = CustomUser
		fields = ['username', 'first_name', 'last_name']
