__author__ = 'jason.parent@carneylabs.com (Jason Parent)'

# Standard library imports...
import time

# Third-party imports...
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.firefox.webdriver import WebDriver

# Django imports...
from django.conf import settings
from django.test import LiveServerTestCase

# Local imports...
from .management.commands.create_session import create_pre_authenticated_session

DEFAULT_WAIT = 5


class FunctionalTest(LiveServerTestCase):
    def setUp(self):
        self.browser = WebDriver()
        self.browser.implicitly_wait(5)

    def tearDown(self):
        self.browser.quit()

    def wait_for(self, function_with_assertion, timeout=DEFAULT_WAIT):
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                return function_with_assertion()
            except (AssertionError, WebDriverException):
                time.sleep(0.1)

        return function_with_assertion()

    def create_pre_authenticated_session(self, email, password, *args, **kwargs):
        session_key = create_pre_authenticated_session(email, password, *args, **kwargs)

        # To set a cookie we need to first visit the domain...
        # 404 pages load the fastest...
        self.browser.get(self.live_server_url + '/404_no_such_url/')
        self.browser.add_cookie({
            'name': settings.SESSION_COOKIE_NAME,
            'value': session_key,
            'path': '/'
        })