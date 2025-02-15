# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
import redis

# Установить переменную окружения Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'email-service.settings')

app = Celery('email-service')

# Загружаем настройки Celery из Django settings
app.conf.BROKER_URL = settings.CELERY_BROKER_URL

# Явно указываем Redis как брокер и бэкенд
app.conf.broker_url = 'redis://localhost:6379/0'
app.conf.result_backend = 'redis://localhost:6379/0'

# Автоматически загружать задачи из зарегистрированных приложений
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Настройки временной зоны
app.conf.timezone = 'Europe/Moscow'
app.conf.enable_utc = True

try:
    app.connection().connect()
    print("Celery успешно подключился к Redis!")
except Exception as e:
    print("Ошибка подключения Celery к Redis: {}".format(e))

# Проверка соединения с Redis
try:
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.ping()
    print("Redis соединение установлено успешно!")
except redis.ConnectionError:
    print("Ошибка соединения с Redis!")
