from django.conf.urls import url, include
from .views import home, logout, login, signup

urlpatterns = [
		url(r'^home/$', home, name='home'),
		url(r'^login/$', login, name='login'),
		url(r'^signup/$', signup, name='signup'),
		url(r'^logout/$', logout, name='logout'),
]
