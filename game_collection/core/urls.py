from django.conf.urls import patterns, include, url
from .views import HomeView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'', HomeView.as_view(), name='home'),
)
