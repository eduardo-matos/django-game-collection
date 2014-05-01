from django import forms
from .models import Game

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class GameForm(forms.ModelForm):

    class Meta:
        model=Game
        fields=('title', 'publisher', 'completed',)
