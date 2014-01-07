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

    def test_form_action_is_create(self):
        resp = self.client.get(r('create'))
        self.assertContains(resp, 'action="' + r('create') + '"')


class UpdateViewTest(TestCase):
    def setUp(self):
        self.game = mommy.make(Game)

    def test_view_exists(self):
        resp = self.client.get(r('update', kwargs={'pk': self.game.pk}))
        self.assertEquals(200, resp.status_code)

    def test_redirects_home_after_saving_game(self):
        resp = self.client.post(r('update', kwargs={'pk': self.game.pk}), {'title': 'a', 'publisher': 'b', 'completed': True})
        self.assertRedirects(resp, r('home'))

    def test_form_action_is_update(self):
        action = r('update', kwargs={'pk': self.game.pk})
        resp = self.client.get(action)
        self.assertContains(resp, 'action="' + action + '"')


class DeleteViewTest(TestCase):
    def setUp(self):
        self.game = mommy.make(Game)

    def test_view_exists(self):
        resp = self.client.get(r('delete', kwargs={'pk': self.game.pk}))
        self.assertEquals(200, resp.status_code)

    def test_show_confirmation_message(self):
        resp = self.client.get(r('delete', kwargs={'pk': self.game.pk}))
        self.assertContains(resp, 'are you sure')

    def test_redirects_home_after_delete(self):
        resp = self.client.post(r('delete', kwargs={'pk': self.game.pk}))
        self.assertRedirects(resp, r('home'))
