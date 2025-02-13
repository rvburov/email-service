from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    url(r'^create-email/$', views.create_email, name='create_email'),
    url(r'^email-list/$', views.email_list, name='email_list'),
    url(r'^subscriber-list/$', views.subscriber_list, name='subscriber_list'),
    url(r'^upload-subscribers/$', views.upload_subscribers, name='upload_subscribers'),
    url(r'^delete-subscriber/(?P<email>[^/]+)$', views.delete_subscriber, name='delete_subscriber'),
]
