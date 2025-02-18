# -*- coding: utf-8 -*-
"""Главные маршруты URL для проекта."""

from django.conf.urls import url, include
from django.contrib import admin
from emails.views import homepage

urlpatterns = [
    # Панель администратора
    url(r'^admin/', admin.site.urls),
    # Маршруты приложения "emails"
    url(r'^emails/', include('emails.urls')),
    # Главная страница
    url(r'^$', homepage, name='home'),
]
