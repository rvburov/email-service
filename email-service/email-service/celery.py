import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'email-service.settings')
app = Celery('email-service')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
