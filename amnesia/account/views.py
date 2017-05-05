from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_http_methods, require_GET, require_POST

from account.forms import LoginForm, SignupForm
from number.forms import PhoneNumberForm
from task.forms import CreateTaskForm
from task.models import REPEAT_CYCLES, SLEEP_CYCLES

# Create your views here.

@require_GET
def landing(request):
	if request.user.is_authenticated():
		return redirect('home')
	return render(request, 'account/landing.html', {'login_form': LoginForm(), 'signup_form': SignupForm(), 'number_form': PhoneNumberForm()})


@require_POST
def login(request):
	if request.user.is_authenticated():
		return redirect('home')
	f = LoginForm(request.POST)
	if f.is_valid():
		user = f.get_user()
		auth_login(request, user)
		return redirect('home')
	else:
		return render(request, 'account/landing.html', {'login_form': f, 'signup_form': SignupForm(), 'number_form': PhoneNumberForm()})

@require_POST
def signup(request):
	if request.user.is_authenticated():
		return redirect('home')
	sf = SignupForm(request.POST)
	nf = PhoneNumberForm(request.POST)
	if sf.is_valid() and nf.is_valid():
		phone_number = nf.save()
		user = sf.save(commit=False)
		user.phone_number = phone_number
		user.save()
		user = authenticate(username=sf.cleaned_data['username'], password=sf.cleaned_data['password2'])
		auth_login(request, user)
		return redirect('home')
	else:
		return render(request, 'account/landing.html', {'login_form': LoginForm(), 'signup_form': sf, 'number_form': nf})

@require_GET
@login_required
def home(request):
	user = request.user
	tasks = []
	logs = user.logs.split('\n')
	logs = [log for log in logs if log]
	for i,task in enumerate(user.tasks.all()):
		tasks.append({
				'number': i+1,
				'created_on': task.created_on,
				'message': task.message,
				'crontab': task.celery_task.crontab.__str__(),
				'repeat': dict(REPEAT_CYCLES)[task.every],
				'sleep_cycle': dict(SLEEP_CYCLES)[task.sleep_cycle],
				'logs': logs,
				})
	return render(request, 'account/home.html', {'tasks': tasks, 'user': user, 'create_task_form': CreateTaskForm(initial={'message':user.get_full_name()}), 'logs':logs})

@require_GET
@login_required
def logout(request):
	auth_logout(request)
	return redirect('landing')
