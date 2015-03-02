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

        # He notices that the navigation bar has a 'users' link that is active.
        link = self.browser.find_element_by_css_selector('li.active')
        link_a = link.find_element_by_tag_name('a')

        self.assertEqual('users-button', link_a.get_attribute('id'))

        # He also notices another navigation bar that has three tabs: search, requests, and browse.
        search_tab = self.browser.find_element_by_id('search_tab')

        self.assertEqual(search_tab.text, 'Search')

        requests_tab = self.browser.find_element_by_id('requests_tab')

        self.assertEqual(requests_tab.text, 'Requests')

        browse_tab = self.browser.find_element_by_id('browse_tab')

        self.assertEqual(browse_tab.text, 'Browse')

    def test_search(self):
        # John is a logged-in user.
        self.create_pre_authenticated_session(
            first_name='John',
            last_name='Carney',
            email='john.carney@carneylabs.com',
            password='password1'
        )

        # John goes to the users page.
        self.browser.get(self.live_server_url + '/users/')

        # He clicks the search button.
        search_tab = self.browser.find_element_by_id('search_tab')
        search_tab.click()

        # The search pane is revealed.
        search_pane = self.browser.find_element_by_id('search_pane')

        self.assertTrue(search_pane.is_displayed())

    def test_requests(self):
        # John is a logged-in user.
        self.create_pre_authenticated_session(
            first_name='John',
            last_name='Carney',
            email='john.carney@carneylabs.com',
            password='password1'
        )

        # John goes to the users page.
        self.browser.get(self.live_server_url + '/users/')

        # He clicks the requests button.
        requests_tab = self.browser.find_element_by_id('requests_tab')
        requests_tab.click()

        # The requests pane is revealed.
        requests_pane = self.browser.find_element_by_id('requests_pane')

        self.assertTrue(requests_pane.is_displayed())

    def test_browse(self):
        # John is a logged-in user.
        self.create_pre_authenticated_session(
            first_name='John',
            last_name='Carney',
            email='john.carney@carneylabs.com',
            password='password1'
        )

        # John goes to the users page.
        self.browser.get(self.live_server_url + '/users/')

        # He clicks the browse button.
        browse_tab = self.browser.find_element_by_id('browse_tab')
        browse_tab.click()

        # The browse pane is revealed.
        browse_pane = self.browser.find_element_by_id('browse_pane')

        self.assertTrue(browse_pane.is_displayed())