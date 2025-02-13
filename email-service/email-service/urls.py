from django.conf.urls import url, include
from django.contrib import admin
from emails.views import homepage

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^emails/', include('emails.urls')),
    url(r'^$', homepage, name='home'),
]