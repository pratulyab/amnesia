from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET

from number.models import Country

# Create your views here.

@require_GET
def get_calling_code(request, country_pk):
	try:
		country = Country.objects.get(pk=country_pk)
	except:
		return JsonResponse(status=400, data={'error': 'Invalid country'})
	return JsonResponse(status=200, data={'calling_code': country.calling_code})
