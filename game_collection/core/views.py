from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy as r
from .models import Game


class ActionMixin(object):
    def get_context_data(self, **kwargs):
        context = super(ActionMixin, self).get_context_data(**kwargs)
        context['action'] = self.get_action()
        return context


class HomeView(ListView):
    model = Game
    template_name = 'core/home.html'


class CreateGameView(ActionMixin, CreateView):
    model = Game
    fields = ('title', 'publisher', 'completed',)
    template_name = 'core/create.html'
    success_url = r('home')

    def get_action(self):
        return r('create')


class UpdateGameView(ActionMixin, UpdateView):
    model = Game
    template_name = 'core/create.html'
    success_url = r('home')

    def get_action(self):
        return r('update', kwargs={'pk': self.object.pk})


class DeleteGameView(DeleteView):
    model = Game
    template_name = 'core/delete.html'
    success_url = r('home')
