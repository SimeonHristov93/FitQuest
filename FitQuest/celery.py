import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitquest.settings')

app = Celery('fit-quest')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()