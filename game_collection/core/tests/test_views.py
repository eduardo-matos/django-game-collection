from django.test import TestCase
from model_mommy import mommy
from core.models import Game
from django.core.urlresolvers import reverse as r

class HomeViewTest(TestCase):
    def test_view_exists(self):
        resp = self.client.get(r('home'))
        self.assertEquals(200, resp.status_code)

    def test_correct_template_used(self):
        resp = self.client.get(r('home'))
        self.assertTemplateUsed('core/home.html', resp)
