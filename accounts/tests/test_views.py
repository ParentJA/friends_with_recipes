__author__ = 'jason.parent@carneylabs.com (Jason Parent)'

# Third-party imports...
from mock import Mock
from mock import patch

# Django imports...
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.test.client import RequestFactory
from django.test import TestCase

# Local imports...
from ..views import home_view
from ..views import log_in_view
from ..views import log_out_view
from ..views import profile_view
from ..views import profile_edit_view
from ..views import sign_up_view

User = get_user_model()


class HomeViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')

    def test_home_view_renders_home_template(self):
        response = home_view(self.request)

        self.assertTemplateUsed(response, 'accounts/home.html')


class SignUpViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        # Valid data...
        data = {
            'first_name': 'John',
            'last_name': 'Carney',
            'email': 'john.carney@carneylabs.com',
            'password1': 'password1',
            'password2': 'password1'
        }

        self.request = self.factory.post('/sign_up/', data)

    def test_sign_up_view_renders_sign_up_template(self):
        request = self.factory.get('/sign_up/')
        response = sign_up_view(request)

        self.assertTemplateUsed(response, 'accounts/sign_up.html')

    @patch('accounts.views.SignUpForm')
    def test_passes_post_data_to_sign_up_form(self, mock_sign_up_form):
        mock_sign_up_form.return_value.is_valid.return_value = False

        sign_up_view(self.request)

        mock_sign_up_form.assert_any_call(data=self.request.POST)

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
        self.factory = RequestFactory()

        # Valid data...
        data = {
            'username': 'john.carney@carneylabs.com',
            'password': 'password1'
        }

        self.request = self.factory.post('/log_in/', data)

    def test_log_in_view_renders_log_in_template(self):
        request = self.factory.get('/log_in/')
        response = log_in_view(request)

        self.assertTemplateUsed(response, 'accounts/log_in.html')

    @patch('accounts.views.LogInForm')
    def test_passes_post_data_to_log_in_form(self, mock_log_in_form):
        mock_log_in_form.return_value.is_valid.return_value = False

        log_in_view(self.request)

        mock_log_in_form.assert_any_call(data=self.request.POST)

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


class ProfileViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_profile_view_renders_profile_template(self):
        request = self.factory.get('/profile/')
        request.user = Mock()
        request.user.return_value.is_authenticated.return_value = True

        response = profile_view(request)

        self.assertTemplateUsed(response, 'accounts/profile.html')


class ProfileEditViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = Mock()
        self.request = self.factory.post('/profile/edit/', {'photo': 'photo'})
        self.request.user = self.user

    def test_profile_edit_view_renders_profile_edit_template(self):
        request = self.factory.get('/profile/edit/')
        request.user = User.objects.create_user(
            username='john.carney@carneylabs.com',
            email='john.carney@carneylabs.com',
            password='password1'
        )

        response = profile_edit_view(request)

        self.assertTemplateUsed(response, 'accounts/profile_edit.html')

    @patch('accounts.views.ProfileForm')
    def test_passes_post_data_and_files_to_profile_form(self, mock_profile_form):
        mock_profile_form.return_value.is_valid.return_value = False

        profile_edit_view(self.request)

        mock_profile_form.assert_any_call(instance=self.user, data=self.request.POST, files=self.request.FILES)

    @patch('accounts.views.ProfileForm')
    def test_does_not_save_form_for_invalid_data(self, mock_profile_form):
        mock_form = mock_profile_form.return_value
        mock_form.is_valid.return_value = False
        mock_form.save.return_value = None

        profile_edit_view(self.request)

        self.assertFalse(mock_form.save.called)

    @patch('accounts.views.ProfileForm')
    def test_saves_form_for_valid_data(self, mock_profile_form):
        mock_form = mock_profile_form.return_value
        mock_form.is_valid.return_value = True
        mock_form.save.return_value = None

        profile_edit_view(self.request)

        self.assertTrue(mock_form.save.called)

    @patch('accounts.views.ProfileForm')
    @patch('accounts.views.render')
    def test_renders_profile_edit_template_for_invalid_data(self, mock_render, mock_profile_form):
        mock_profile_form.return_value.is_valid.return_value = False

        response = profile_edit_view(self.request)

        self.assertEqual(response, mock_render.return_value)

        mock_render.assert_called_once_with(self.request, 'accounts/profile_edit.html', {
            'form': mock_profile_form.return_value
        })

    @patch('accounts.views.ProfileForm')
    @patch('accounts.views.redirect')
    def test_redirects_profile_for_valid_data(self, mock_redirect, mock_profile_form):
        mock_form = mock_profile_form.return_value
        mock_form.is_valid.return_value = True
        mock_form.save.return_value = None

        response = profile_edit_view(self.request)

        self.assertTrue(mock_redirect.called)
        self.assertEqual(response, mock_redirect.return_value)