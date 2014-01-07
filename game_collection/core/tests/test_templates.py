from django.test import TestCase
from model_mommy import mommy
from core.models import Game
from django.core.urlresolvers import reverse as r

class HomeTemplate(TestCase):
    def test_template_lists_games(self):
        mommy.make(Game, _quantity=5)
        resp = self.client.get(r('home'))
        self.assertContains(resp, '<tr', 6)

    def test_template_show_message_if_there_is_no_games(self):
        resp = self.client.get(r('home'))
        self.assertContains(resp, 'There are no games')
