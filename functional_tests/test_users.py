__author__ = 'jason.parent@carneylabs.com (Jason Parent)'

# Local imports...
from .base import FunctionalTest


class UsersTest(FunctionalTest):
    def test_users_view(self):
        # John is a logged-in user.
        self.create_pre_authenticated_session(
            first_name='John',
            last_name='Carney',
            email='john.carney@carneylabs.com',
            password='password1'
        )

        # John goes to the users page.
        self.browser.get(self.live_server_url + '/users/')

        # He notices that the page title says 'Users'.
        title = self.browser.find_element_by_tag_name('title')

        self.assertIn('Users', title.text)