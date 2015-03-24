__author__ = 'jason.parent@carneylabs.com (Jason Parent)'

# Django imports...
from django.contrib.auth import get_user_model

# Local imports...
from .base import FunctionalTest

User = get_user_model()


class AuthenticationTest(FunctionalTest):
    def test_sign_up(self):
        # John goes to the sign up page.
        self.browser.get(self.live_server_url + '/sign_up/')

        # He notices a form with fields to input first name, last name, email, and passwords.
        # There is also a button that says 'Sign up'.
        # John adds his data and clicks the 'Sign up' button.
        self.browser.find_element_by_id('id_first_name').send_keys('John')
        self.browser.find_element_by_id('id_last_name').send_keys('Carney')
        self.browser.find_element_by_id('id_email').send_keys('john.carney@carneylabs.com')
        self.browser.find_element_by_id('id_password1').send_keys('password1')
        self.browser.find_element_by_id('id_password2').send_keys('password1')

        submit = self.browser.find_element_by_id('sign_up_button')

        self.assertEqual(submit.text, 'Sign up')

        submit.click()

        # The page refreshes and John sees a welcome message with his name in the navigation bar,
        # along with a menu button.
        navbar = self.browser.find_element_by_class_name('navbar-text')

        self.assertIn('Signed in as John', navbar.text)

        menu = self.browser.find_element_by_id('menu_button')
        menu.click()

        log_out = self.browser.find_element_by_id('log_out_button')

        self.assertEqual(log_out.text, 'Log out')

    def test_log_in(self):
        # John has previously signed up for an account, but he is not logged in.
        User.objects.create_user(
            first_name='John',
            last_name='Carney',
            username='john.carney@carneylabs.com',
            email='john.carney@carneylabs.com',
            password='password1'
        )

        # He goes to the log in page.
        self.browser.get(self.live_server_url + '/log_in/')

        # He notices a form with fields to input username and password.
        # There is also a button that says 'Log in'.
        # John adds his data and clicks the 'Log in' button.
        self.browser.find_element_by_id('id_username').send_keys('john.carney@carneylabs.com')
        self.browser.find_element_by_id('id_password').send_keys('password1')

        submit = self.browser.find_element_by_id('log_in_button')

        self.assertEqual(submit.text, 'Log in')

        submit.click()

        # The page refreshes and John sees a welcome message with his name in the navigation bar,
        # along with a menu button.
        navbar = self.browser.find_element_by_class_name('navbar-text')

        self.assertIn('Signed in as John', navbar.text)

        menu = self.browser.find_element_by_id('menu_button')
        menu.click()

        log_out = self.browser.find_element_by_id('log_out_button')

        self.assertEqual(log_out.text, 'Log out')

    def test_log_out(self):
        # John is a logged-in user.
        self.create_pre_authenticated_session(
            first_name='John',
            last_name='Carney',
            email='john.carney@carneylabs.com',
            password='password1'
        )

        # John goes to the home page.
        self.browser.get(self.live_server_url)

        # He sees a welcome message with his name in the navigation bar, along with a menu button.
        navbar = self.browser.find_element_by_class_name('navbar-text')

        self.assertIn('Signed in as John', navbar.text)

        menu = self.browser.find_element_by_id('menu_button')
        menu.click()

        log_out = self.browser.find_element_by_id('log_out_button')

        self.assertEqual(log_out.text, 'Log out')

        # John clicks the 'Log out' button.
        log_out.click()

        # The page refreshes and John notices that he is back on the home page and is logged out.
        # He sees a 'Log in' button and a 'Sign up' button.
        log_in = self.browser.find_element_by_id('log_in_button')

        self.assertEqual(log_in.text, 'Log in')

        sign_up = self.browser.find_element_by_id('sign_up_button')

        self.assertEqual(sign_up.text, 'Sign up')

    def test_user_can_visit_home_as_logged_in_user(self):
        # John is a logged-in user.
        self.create_pre_authenticated_session(
            first_name='John',
            last_name='Carney',
            email='john.carney@carneylabs.com',
            password='password1'
        )

        # John goes to the home page.
        self.browser.get(self.live_server_url)

        # He sees a button that says "Continue to Feed".
        feed_button = self.browser.find_element_by_id('feed_button')

        self.assertEqual(feed_button.text, 'Continue to Feed')