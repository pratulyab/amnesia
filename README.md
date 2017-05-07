# Amnesia

## 1) To schedule tasks
- Using celery as distributed task queue
- Celery Crontabs to schedule task

## 2) Redis Backend as broker

## 3) SMS Service - TWILIO
- Python library
- Add your TWILIO credentials to amnesia/settings.py
	- TWILIO_ACCOUNT_SID
	- TWILIO_AUTH_TOKEN
	- MY_TWILIO_NUMBER
- Utils in sms.py
- SMS task => task/tasks.py

## 4) How To Run:
- Make sure to have redis-server installed. Run redis-server
- Run django's local server and visit localhost
- Signup + Login
	- If working with existing database:
		- User:
			- username: john
			- password: john
		- Superuser:
			- username: admin
			- password: admin
- Create Task
	- "Message" Field
		- What message should be sent
	- "Repeat Every" Field
		- Choose from:
			- every minute
			- 15 minutes
			- 30 minutes
			- 60 minutes (hour) (the original requirement)
	- "Sleep Cycle" Field
		- As the problem states, the message should not be sent when the user is asleep. Assuming sleep cycle of 8 hours, choose from:
			- None (No night hours restriction)
			- 8pm - 4am
			- ...
		- Complementary hours are used for crontab

- Run "celery -A amnesia worker -l info" to boot workers.
- Run "celery -A amnesia beat -l info -S django" to start scheduling using celery beat.
	- "-S" is used to specify the scheduler
	- which in this case is django
- Wait to be notified on your registered and Twilio verified number.
- Both SUCCESS and FAILURE logs will be outputted to user's homepage.

## 5) Django Things:
- Inorder to create superuser, use django shell. Each user has a OneToOne mapping to a PhoneNumber.
- FIXTURES: number/fixtures/countries.json =>
	- Country name
	- Alpha-2 Codes
	- Calling Codes
- countries.py scrapes wikipedia pages for above data.

## 6) Point of Failure:
- Server works with Asia/Kolkata as TIMEZONE. So, if user of different TZ schedules a task, the schedule would work according to the server's TIMEZONE.
- (Working with UTC would also have same implications)
- Currently, django_celery_beat doesn't seem to support 'nowfun' argument for crontab scheduling which helps in making tasks aware of TZ.
- However, to check for the TIMEZONE offset, a hidden input is received when "Create Task Form" is submitted. (name="timezone_offset")
- Leaving it because otherwise the solution ceases to be basic.

## 7) Disclaimer:
- Celery Beat process needs to be restarted for new task. (django-celery-beat's limitation)
	- Can implement a work around, but then the application would cease to be basic.
- SQLite3 db is used for portability and easy demonstration purposes.
- The UI is shabby. The internship demands backend SE.
- "Logs" has been merged shamelessly within the user model for simplicity purposes.
- Not much user authentication is applied because a basic application is required.
- The Twilio Lookup API's validation can be improved.
