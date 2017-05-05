from django.contrib import admin

from number.models import Country, PhoneNumber
# Register your models here.

admin.site.register(Country)
admin.site.register(PhoneNumber)
