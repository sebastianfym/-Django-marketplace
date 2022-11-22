import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('data_import')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
