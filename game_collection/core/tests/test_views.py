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


class CreateViewTest(TestCase):
    def test_view_exists(self):
        resp = self.client.get(r('create'))
        self.assertEquals(200, resp.status_code)

    def test_get_request_shows_form(self):
        resp = self.client.get(r('create'))
        self.assertContains(resp, '<form')
        self.assertContains(resp, 'name="title"')
        self.assertContains(resp, 'name="publisher"')
        self.assertContains(resp, 'name="completed"')

    def test_can_create_game(self):
        game_data = {'title': 'My Title', 'publisher': 'Pub', 'completed': True}
        resp = self.client.post(r('create'), game_data)
        self.assertEquals(Game.objects.count(), 1)

    def test_redirect_home_after_saving(self):
        game_data = {'title': 'My Title', 'publisher': 'Pub', 'completed': True}
        resp = self.client.post(r('create'), game_data, follow=True)
        self.assertRedirects(resp, r('home'))

    def test_show_errors_if_data_do_not_validate(self):
        game_data = {'title': '', 'publisher': '', 'completed': True}
        resp = self.client.post(r('create'), game_data)
        self.assertContains(resp, 'error')
