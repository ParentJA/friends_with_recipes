__author__ = 'jason.parent@carneylabs.com (Jason Parent)'

# Django imports...
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest
from django.test import TestCase

# Local imports...
from ..forms import LogInForm
from ..forms import ProfileForm
from ..forms import SignUpForm

User = get_user_model()


class LogInFormTest(TestCase):
    def setUp(self):
        self.email = 'john.carney@carneylabs.com'
        self.password = 'password1'
        self.user = User.objects.create_user(username=self.email, email=self.email, password=self.password)
        self.request = HttpRequest()
        self.request.user = self.user

    def test_form_has_username_and_password_fields(self):
        form = LogInForm()

        self.assertIn('id="id_username"', form.as_p())
        self.assertIn('id="id_password"', form.as_p())

    def test_form_does_not_validate_for_empty_fields(self):
        form = LogInForm(data=self.request.POST)

        self.assertFalse(form.is_valid())

    def test_form_does_not_validate_for_incorrect_password(self):
        self.request.POST['username'] = self.email
        self.request.POST['password'] = 'wrong password'

        form = LogInForm(data=self.request.POST)

        self.assertFalse(form.is_valid())

    def test_form_validates_for_correct_username_and_password(self):
        self.request.POST['username'] = self.email
        self.request.POST['password'] = self.password

        form = LogInForm(data=self.request.POST)

        self.assertTrue(form.is_valid())


class SignUpFormTest(TestCase):
    def setUp(self):
        self.first_name = 'John'
        self.last_name = 'Carney'
        self.email = 'john.carney@carneylabs.com'
        self.password = 'password1'
        self.request = HttpRequest()
        self.request.user = AnonymousUser()

    def test_form_has_required_fields(self):
        form = SignUpForm()

        self.assertIn('id="id_first_name"', form.as_p())
        self.assertIn('id="id_last_name"', form.as_p())
        self.assertIn('id="id_email"', form.as_p())
        self.assertIn('id="id_password1"', form.as_p())
        self.assertIn('id="id_password2"', form.as_p())

    def test_form_does_not_validate_for_empty_fields(self):
        form = SignUpForm(data=self.request.POST)

        self.assertFalse(form.is_valid())

    def test_form_raises_error_on_duplicate_email(self):
        User.objects.create_user(username=self.email, email=self.email, password=self.password)

        self.request.POST = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'password1': self.password,
            'password2': self.password
        }

        form = SignUpForm(data=self.request.POST)

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'][0], SignUpForm.error_messages['duplicate_email'])

    def test_form_raises_error_on_password_mismatch(self):
        self.request.POST = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'password1': self.password,
            'password2': 'different password'
        }

        form = SignUpForm(data=self.request.POST)

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password2'][0], SignUpForm.error_messages['password_mismatch'])

    def test_form_validates_and_creates_user_for_good_data(self):
        self.request.POST = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'password1': self.password,
            'password2': self.password
        }

        form = SignUpForm(data=self.request.POST)

        self.assertTrue(form.is_valid())

        user = form.save()

        self.assertEqual(user.email, self.email)


class ProfileFormTest(TestCase):
    def test_form_has_required_fields(self):
        form = ProfileForm()

        self.assertIn('id="id_photo"', form.as_p())