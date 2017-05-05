from django.conf.urls import url, include
from .views import get_calling_code

urlpatterns = [
		url(r'^get_cc/(?P<country_pk>\d+)/$', get_calling_code, name='calling_code'),
]
