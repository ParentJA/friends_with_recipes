__author__ = 'jason.parent@carneylabs.com (Jason Parent)'

# Third-party imports...
from selenium.webdriver.firefox.webdriver import WebDriver

# Django imports...
from django.test import LiveServerTestCase


class LoginTest(LiveServerTestCase):
    def setUp(self):
        self.browser = WebDriver()
        self.browser.implicitly_wait(5)

    def tearDown(self):
        self.browser.quit()

    def test_login(self):
        # John goes to the home page.
        self.browser.get(self.live_server_url)