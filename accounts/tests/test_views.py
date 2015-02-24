__author__ = 'jason.parent@carneylabs.com (Jason Parent)'

# Third-party imports...
from mock import Mock
from mock import patch

# Django imports...
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest
from django.test import TestCase

# Local imports...
from ..views import log_in_view
from ..views import log_out_view
from ..views import sign_up_view

User = get_user_model()


class HomeViewTest(TestCase):
    def test_home_view_renders_home_template(self):
        response = self.client.get('/')

        self.assertTemplateUsed(response, 'accounts/home.html')


class SignUpViewTest(TestCase):
    def setUp(self):
        self.request = HttpRequest()
        self.request.POST['first_name'] = 'John'
        self.request.POST['last_name'] = 'Carney'
        self.request.POST['email'] = 'john.carney@carneylabs.com'
        self.request.POST['password1'] = 'password1'
        self.request.POST['password2'] = 'password1'
        self.request.user = AnonymousUser()

    def test_sign_up_view_renders_sign_up_template(self):
        response = self.client.get('/sign_up/')

        self.assertTemplateUsed(response, 'accounts/sign_up.html')

    @patch('accounts.views.SignUpForm')
    @patch('accounts.views.login')
    def test_does_not_save_form_or_log_in_user_for_invalid_data(self, mock_login, mock_sign_up_form):
        mock_form = mock_sign_up_form.return_value
        mock_form.is_valid.return_value = False
        mock_form.save.return_value = Mock()

        sign_up_view(self.request)

        self.assertFalse(mock_form.save.called)
        self.assertFalse(mock_login.called)

    @patch('accounts.views.SignUpForm')
    @patch('accounts.views.login')
    def test_saves_form_and_logs_in_user_for_valid_data(self, mock_login, mock_sign_up_form):
        mock_form = mock_sign_up_form.return_value
        mock_form.is_valid.return_value = True
        mock_form.save.return_value = Mock(email='john.carney@carneylabs.com')

        sign_up_view(self.request)

        self.assertTrue(mock_form.save.called)

        mock_login.assert_called_once_with(self.request, mock_form.save.return_value)

    @patch('accounts.views.SignUpForm')
    @patch('accounts.views.render')
    def test_renders_sign_up_template_for_invalid_data(self, mock_render, mock_sign_up_form):
        mock_sign_up_form.return_value.is_valid.return_value = False

        response = sign_up_view(self.request)

        self.assertEqual(response, mock_render.return_value)

        mock_render.assert_called_once_with(self.request, 'accounts/sign_up.html', {
            'form': mock_sign_up_form.return_value
        })

    @patch('accounts.views.SignUpForm')
    @patch('accounts.views.login')
    @patch('accounts.views.redirect')
    def test_redirects_home_for_valid_data(self, mock_redirect, mock_login, mock_sign_up_form):
        mock_form = mock_sign_up_form.return_value
        mock_form.is_valid.return_value = True
        mock_form.save.return_value = Mock()

        response = sign_up_view(self.request)

        self.assertTrue(mock_redirect.called)
        self.assertEqual(response, mock_redirect.return_value)


class LogInViewTest(TestCase):
    def setUp(self):
        self.request = HttpRequest()
        self.request.POST['username'] = 'john.carney@carneylabs.com'
        self.request.POST['password'] = 'password1'
        self.request.user = AnonymousUser()

    def test_log_in_view_renders_log_in_template(self):
        response = self.client.get('/log_in/')

        self.assertTemplateUsed(response, 'accounts/log_in.html')

    @patch('accounts.views.LogInForm')
    @patch('accounts.views.login')
    def test_does_not_log_in_user_for_invalid_data(self, mock_login, mock_log_in_form):
        mock_form = mock_log_in_form.return_value
        mock_form.is_valid.return_value = False
        mock_form.get_user.return_value = None

        log_in_view(self.request)

        self.assertFalse(mock_form.get_user.called)
        self.assertFalse(mock_login.called)

    @patch('accounts.views.LogInForm')
    @patch('accounts.views.login')
    def test_logs_in_user_for_valid_data(self, mock_login, mock_log_in_form):
        mock_form = mock_log_in_form.return_value
        mock_form.is_valid.return_value = True
        mock_form.get_user.return_value = Mock(email='john.carney@carneylabs.com')

        log_in_view(self.request)

        self.assertTrue(mock_form.get_user.called)

        mock_login.assert_called_once_with(self.request, mock_form.get_user.return_value)

    @patch('accounts.views.LogInForm')
    @patch('accounts.views.render')
    def test_renders_log_in_template_for_invalid_data(self, mock_render, mock_log_in_form):
        mock_log_in_form.return_value.is_valid.return_value = False

        response = log_in_view(self.request)

        self.assertEqual(response, mock_render.return_value)

        mock_render.assert_called_once_with(self.request, 'accounts/log_in.html', {
            'form': mock_log_in_form.return_value
        })

    @patch('accounts.views.LogInForm')
    @patch('accounts.views.login')
    @patch('accounts.views.redirect')
    def test_redirects_home_for_valid_data(self, mock_redirect, mock_login, mock_log_in_form):
        mock_form = mock_log_in_form.return_value
        mock_form.is_valid.return_value = True
        mock_form.save.return_value = Mock()

        response = log_in_view(self.request)

        self.assertTrue(mock_redirect.called)
        self.assertEqual(response, mock_redirect.return_value)


class LogOutViewTest(TestCase):
    @patch('accounts.views.redirect')
    @patch('accounts.views.logout')
    def test_log_out_view_logs_out_user_and_redirects_to_home_page(self, mock_logout, mock_redirect):
        request = HttpRequest()
        request.user = Mock()

        response = log_out_view(request)

        mock_logout.assert_called_once_with(request)

        self.assertTrue(mock_redirect.called)
        self.assertEqual(response, mock_redirect.return_value)