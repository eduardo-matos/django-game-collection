from django.test import TestCase
from model_mommy import mommy
from core.models import Game

class GameTest(TestCase):
    def test_unicode(self):
        game = mommy.make(Game, title='My Title')
        self.assertEquals('My Title', unicode(game))
