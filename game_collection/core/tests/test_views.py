from django.test import TestCase
from model_mommy import mommy
from core.models import Game
from django.core.urlresolvers import reverse as r
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from django.test.client import RequestFactory
from ..views import LoginView


User = get_user_model()


def create_user(client=None, with_game=True):
    user = User.objects.create_user(username='egg', password='egg')

    if with_game:
        game = mommy.make(Game, owner=user)
    else:
        game = None

    if client:
        client.login(username='egg', password='egg')

    return (user, game,)


class LoginViewTest(TestCase):
    def test_page_must_exist(self):
        resp = self.client.get(r('login'))
        self.assertEquals(200, resp.status_code)

    def test_form_has_fields(self):
        resp = self.client.get(r('login'))
        # csrf, username, password, submit
        self.assertContains(resp, '<input', 4)


class LogoutTestView(TestCase):
    def test_redirect_login_after_logout(self):
        user, _ = create_user(self.client, with_game=False)

        resp = self.client.get(r('logout'), follow=True)
        self.assertEquals(302, resp.redirect_chain[0][1])

        self.assertTrue(r('login') in resp.redirect_chain[-1][0])

class HomeViewTest(TestCase):
    def setUp(self):
        self.user, _ = create_user(self.client, False)

    def test_response_is_302_if_user_isnt_logged_in(self):
        self.client.logout()
        resp = self.client.get(r('home'))
        self.assertEquals(302, resp.status_code)

    def test_response_is_200_if_user_is_logged_in(self):
        resp = self.client.get(r('home'))
        self.assertEquals(200, resp.status_code)

    def test_correct_template_used(self):
        resp = self.client.get(r('home'))
        self.assertTemplateUsed('core/home.html', resp)

    def test_list_only_games_owned_by_logged_user(self):
        user2 = User.objects.create_user(username='foo', password='bar')
        mommy.make(Game, _quantity=5, owner=self.user)
        mommy.make(Game, _quantity=4, owner=user2)

        resp = self.client.get(r('home'))

        self.assertEquals(5, len(resp.context['object_list']))


class CreateViewTest(TestCase):
    def setUp(self):
        self.user, _ = create_user(self.client, False)

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
        self.assertEquals(Game.objects.all().first().owner, self.user)

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
        self.user, self.game = create_user(self.client, True)

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

    def test_response_is_404_if_logged_user_doesnt_own_game(self):
        game2 = mommy.make(Game)

        resp1 = self.client.get(r('update', kwargs={'pk': game2.pk}))
        self.assertEquals(404, resp1.status_code)

        resp2 = self.client.post(r('update', kwargs={'pk': game2.pk}), {'title': 'a', 'publisher': 'b', 'completed': True})
        self.assertEquals(404, resp2.status_code)


class DeleteViewTest(TestCase):
    def setUp(self):
        self.user, self.game = create_user(self.client, True)

    def test_view_exists(self):
        resp = self.client.get(r('delete', kwargs={'pk': self.game.pk}))
        self.assertEquals(200, resp.status_code)

    def test_show_confirmation_message(self):
        resp = self.client.get(r('delete', kwargs={'pk': self.game.pk}))
        self.assertContains(resp, 'are you sure')

    def test_redirects_home_after_delete(self):
        resp = self.client.post(r('delete', kwargs={'pk': self.game.pk}))
        self.assertRedirects(resp, r('home'))

    def test_response_is_404_if_logged_user_doesnt_own_game(self):
        user2 = User.objects.create_user(username='foo', password='bar')
        game2 = mommy.make(Game, owner=user2)

        resp1 = self.client.get(r('delete', kwargs={'pk': game2.pk}))
        self.assertEquals(404, resp1.status_code)

        resp2 = self.client.post(r('delete', kwargs={'pk': game2.pk}))
        self.assertEquals(404, resp2.status_code)
