from django.conf.urls import patterns, include, url
from .views import HomeView, CreateGameView, UpdateGameView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'create/$', CreateGameView.as_view(), name='create'),
    url(r'update/(?P<pk>\d+)', UpdateGameView.as_view(), name='update'),
    url(r'$', HomeView.as_view(), name='home'),
)
