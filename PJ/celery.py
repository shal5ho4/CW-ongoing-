import os
from unicodedata import name
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PJ.settings')

app = Celery('PJ')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
