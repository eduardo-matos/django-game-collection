from django.test import TestCase
from model_mommy import mommy
from core.models import Game
from django.contrib.auth import get_user_model

User = get_user_model()

class GameTest(TestCase):
    def test_unicode(self):
        game = mommy.make(Game, title='My Title')
        self.assertEquals('My Title', unicode(game))

    def test_game_must_be_associated_with_an_user(self):
        game = mommy.make(Game, title='My Title')
        self.assertIsInstance(game.owner, User)
