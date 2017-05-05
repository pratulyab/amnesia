from django.db import models

# Create your models here.

class Country(models.Model):
	name = models.CharField(max_length=128, unique=True)
	code = models.CharField(max_length=2, unique=True) # Alpha - 2 codes
	calling_code = models.CharField(max_length=4) # Max length 4 because DB will contain only the country codes, and not the area codes

	def __str__(self):
		return "%s [%s]" % (self.name, self.code)

	class Meta:
		verbose_name_plural = "Countries"

class PhoneNumber(models.Model):
	number = models.CharField(max_length=10, unique=True)
	area_code = models.CharField(max_length=5, blank=True)
	country = models.ForeignKey(Country, related_name="numbers")

	def __str__(self):
		return "(%s)%s" % (self.country.calling_code, self.number)
