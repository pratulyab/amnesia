from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from task.forms import CreateTaskForm
from task.models import REPEAT_CYCLES, SLEEP_CYCLES

import math

# Create your views here.

@login_required
@require_POST
def create_task(request):
	user = request.user
	f = CreateTaskForm(request.POST)
	fraction, whole = math.modf(float(request.POST.get('timezone_offset', 0)))
	print(whole, fraction)
	if f.is_valid():
		f.save(user=user)
		return redirect('home')
	else:
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
		return render(request, 'account/home.html', {'tasks': tasks, 'user': user, 'create_task_form': f})
