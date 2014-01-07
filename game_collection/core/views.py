from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Game

class HomeView(ListView):
    model = Game
    template_name = 'core/home.html'
