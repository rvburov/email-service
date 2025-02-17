# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
import redis

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'email-service.settings')
app = Celery('email-service')
app.conf.BROKER_URL = settings.CELERY_BROKER_URL
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

try:
    app.connection().connect()
    print("Celery успешно подключился к Redis!")
except Exception as e:
    print("Ошибка подключения Celery к Redis: {}".format(e))

try:
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.ping()
    print("Redis соединение установлено успешно!")
except redis.ConnectionError:
    print("Ошибка соединения с Redis!")
