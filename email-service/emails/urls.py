# -*- coding: utf-8 -*-
"""Маршруты URL для системы email-рассылок."""

from django.conf.urls import url
from . import views

urlpatterns = [
    # Главная страница
    url(r'^$', views.homepage, name='homepage'),
    # Управление email-рассылками
    url(r'^create-email/$',
        views.create_email,
        name='create_email'
    ),
    url(r'^email-list/$',
        views.email_list,
        name='email_list'
    ),
    # Управление подписчиками
    url(r'^subscriber-list/$',
        views.subscriber_list,
        name='subscriber_list'
    ),
    url(
        r'^upload-subscribers/$',
        views.upload_subscribers,
        name='upload_subscribers'
    ),
    url(
        r'^delete-subscriber/(?P<email>[^/]+)$',
        views.delete_subscriber,
        name='delete_subscriber'
    ),
    # Отслеживание открытия писем
    url(
        r'^track-open/(?P<mailing_id>\d+)/(?P<subscriber_id>\d+)/$',
        views.track_email_open,
        name='track_email_open'
    ),
]
