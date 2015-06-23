__author__ = 'parentj@eab.com (Jason Parent)'

# Django imports...
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.client import RequestFactory

# Local imports...
from ..views import home_view

User = get_user_model()


class HomeViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/recipes/')
        self.request.user = User.objects.create_user(
            username='parentj@eab.com',
            email='parentj@eab.com',
            password='pAssw0rd'
        )

    def test_home_view_renders_home_template(self):
        response = home_view(self.request)

        self.assertTemplateUsed(response, 'recipes/home.html')