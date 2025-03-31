from celery import Celery
from celery.schedules import crontab

app = Celery('tasks', broker='redis://localhost:6379/0')

app.conf.beat_schedule = {
    'send-monthly-report': {
        'task': 'tasks.send_monthly_report',
        'schedule': crontab(day_of_month=1, hour=0, minute=0),  # Runs on the 1st of every month at midnight
    },
}

app.conf.timezone = 'Asia/Kolkata'  # Set to your timezone


#redis-server (make sure it is running)

#Run the Celery Worker In PowerShell, start the Celery worker by running:
#celery -A tasks worker --loglevel=info

#Run the Celery Beat Scheduler In a new PowerShell window, run:
#celery -A tasks beat --loglevel=info

