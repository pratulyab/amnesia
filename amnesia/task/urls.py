from django.conf.urls import url, include
from .views import create_task

urlpatterns = [
		url(r'^create/$', create_task, name='create_task'),
]
