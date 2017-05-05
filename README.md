# Amnesia

##1) To schedule tasks
- Using celery as distributed task queue
- Celery Crontabs to schedule task

##2) Redis Backend as broker

##3) SMS Service - TWILIO
- Python library
- Add your TWILIO credentials to amnesia/settings.py
	- TWILIO_ACCOUNT_SID
	- TWILIO_AUTH_TOKEN
	- MY_TWILIO_NUMBER

##4) How To Run:
- Make sure to have redis-server installed. Run redis-server
- Run "celery -A amnesia worker -l info" to boot workers.
- Run "celery -A amnesia beat -l info -S django" to start scheduling using celery beat.
- Visit localhost
- Signup + Login
- Create Task

##5) Django Things:
- Inorder to create superuser, use django shell. Each user has a OneToOne mapping to a PhoneNumber.
- FIXTURES: number/fixtures/countries.json =>
	- Country name
	- Alpha-2 Code
- countries.py scrapes wikipedia pages for above data.

##6) Point of Failure:
- Server stores works with Asia/Kolkata as TIMEZONE
- If user of different TZ schedules a task, the schedule would work according to the server's TIMEZONE.
- Currently, django_celery_beat doesn't seem to support 'nowfun' argument for crontab scheduling. 
- Also, leaving it because otherwise the solution ceases to be basic.
- However, to check for the TIMEZONE offset, a hidden input is received when "Create Task Form" is submitted. (name="timezone_offset")

##7) Disclaimer:
- The UI is shabby. The internship demands backend SE.
- "Logs" has been merged shamelessly within the user model for simplicity purposes.
- Not much user authentication is applied because a basic application is required.
- The Twilio Lookup API's validation can be improved.
