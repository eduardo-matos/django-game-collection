from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy as r
from .models import Game

class HomeView(ListView):
    model = Game
    template_name = 'core/home.html'


class CreateGameView(CreateView):
    model = Game
    fields = ('title', 'publisher', 'completed',)
    template_name = 'core/create.html'
    success_url = r('home')
