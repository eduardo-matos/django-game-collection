from django.conf.urls import patterns, include, url
from .views import (LoginView, LogoutView, HomeView,
    CreateGameView, UpdateGameView, DeleteGameView)

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'login/$', LoginView.as_view(), name='login'),
    url(r'logout/$', LogoutView.as_view(), name='logout'),
    url(r'create/$', CreateGameView.as_view(), name='create'),
    url(r'update/(?P<pk>\d+)', UpdateGameView.as_view(), name='update'),
    url(r'delete/(?P<pk>\d+)', DeleteGameView.as_view(), name='delete'),
    url(r'$', HomeView.as_view(), name='home'),
)
