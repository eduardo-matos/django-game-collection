from django.http import Http404
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.base import RedirectView
from django.core.urlresolvers import reverse_lazy as r
from django.contrib.auth import authenticate, login, logout
from .models import Game
from .forms import LoginForm, GameForm
from braces.views import LoginRequiredMixin


class ActionMixin(object):
    def get_context_data(self, **kwargs):
        context = super(ActionMixin, self).get_context_data(**kwargs)
        context['action'] = self.get_action()
        return context


class LoginView(FormView):
    template_name = 'core/login.html'
    form_class = LoginForm
    success_url = r('home')

    def get(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated():
            return HttpResponseRedirect(self.success_url)

        return super(LoginView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        username = self.request.POST.get('username', '')
        password = self.request.POST.get('password', '')

        user = authenticate(username=username, password=password)

        if user and user.is_active:
            login(self.request, user)
            return super(LoginView, self).form_valid(form)

        return render(self.request, self.template_name, {'form': form})


class LogoutView(RedirectView):
    url = r('login')
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return super(LogoutView, self).get_redirect_url(*args, **kwargs)


class HomeView(LoginRequiredMixin, ListView):
    model = Game
    template_name = 'core/home.html'

    def get_queryset(self):
        qs = super(HomeView, self).get_queryset()
        return qs.filter(owner=self.request.user)


class CreateGameView(LoginRequiredMixin, ActionMixin, CreateView):
    model = Game
    fields = ('title', 'publisher', 'completed',)
    template_name = 'core/create.html'
    success_url = r('home')

    def form_valid(self, form):
        game = form.save(commit=False)
        game.owner = self.request.user
        game.save()
        return super(CreateGameView, self).form_valid(form)

    def get_action(self):
        return r('create')


class UpdateGameView(LoginRequiredMixin, ActionMixin, UpdateView):
    model = Game
    form_class = GameForm
    template_name = 'core/create.html'
    success_url = r('home')

    def get_action(self):
        return r('update', kwargs={'pk': self.object.pk})

    def get_object(self):
        game = super(UpdateView, self).get_object()
        if game.owner == self.request.user:
            return game
        raise Http404()


class DeleteGameView(LoginRequiredMixin, DeleteView):
    model = Game
    template_name = 'core/delete.html'
    success_url = r('home')

    def get_object(self):
        game = super(DeleteGameView, self).get_object()
        if game.owner == self.request.user:
            return game
        raise Http404()
