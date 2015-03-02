__author__ = 'jason.parent@carneylabs.com (Jason Parent)'

# Django imports...
from django.contrib.auth import get_user_model
from django.test.client import RequestFactory
from django.test import Client
from django.test import TestCase

# Local imports...
from ..views import home_view

User = get_user_model()


class HomeViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/users/')
        self.request.user = User.objects.create_user(
            username='john.carney@carneylabs.com',
            email='john.carney@carneylabs.com',
            password='password1'
        )

    def test_home_view_renders_home_template(self):
        response = home_view(self.request)

        self.assertTemplateUsed(response, 'users/home.html')


class ListViewTest(TestCase):
    def setUp(self):
        User.objects.create_user(
            username='john.carney@carneylabs.com',
            email='john.carney@carneylabs.com',
            password='password1'
        )

        self.client = Client()
        self.client.login(username='john.carney@carneylabs.com', password='password1')

    def test_list_view_renders_list_template(self):
        response = self.client.get('/users/list/')

        self.assertTemplateUsed(response, 'users/list.html')

    def test_list_view_returns_empty_list_for_invalid_search(self):
        response = self.client.get('/users/list/?search=nonexistent')

        self.assertListEqual(list(response.context['users']), [])

    def test_list_view_returns_valid_list_for_valid_search(self):
        regina = User.objects.create_user(
            username='regina.mcdonalid93@example.com',
            email='regina.mcdonalid93@example.com',
            password='password1'
        )

        User.objects.create_user(
            username='travis.mills57@example.com',
            email='travis.mills57@example.com',
            password='password1'
        )

        response = self.client.get('/users/list/?search=regina')

        self.assertIn(regina, response.context['users'])

    def test_list_view_returns_all_users_except_request_user_on_empty_search(self):
        regina = User.objects.create_user(
            username='regina.mcdonalid93@example.com',
            email='regina.mcdonalid93@example.com',
            password='password1'
        )

        travis = User.objects.create_user(
            username='travis.mills57@example.com',
            email='travis.mills57@example.com',
            password='password1'
        )

        response = self.client.get('/users/list/')

        self.assertIn(regina, response.context['users'])
        self.assertIn(travis, response.context['users'])