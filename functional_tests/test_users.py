__author__ = 'jason.parent@carneylabs.com (Jason Parent)'

# Django imports...
from django.contrib.auth import get_user_model

# Local imports...
from .base import FunctionalTest

User = get_user_model()


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

        # He also notices another navigation bar that has four tabs: search, requests, browse, and friends.
        search_tab = self.browser.find_element_by_id('search_tab')

        self.assertEqual(search_tab.text, 'Search')

        requests_tab = self.browser.find_element_by_id('requests_tab')

        self.assertEqual(requests_tab.text, 'Requests')

        browse_tab = self.browser.find_element_by_id('browse_tab')

        self.assertEqual(browse_tab.text, 'Browse')

        friends_tab = self.browser.find_element_by_id('friends_tab')

        self.assertEqual(friends_tab.text, 'Friends')

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

        # He clicks the search tab.
        search_tab = self.browser.find_element_by_id('search_tab')
        search_tab.click()

        # The search pane is revealed.
        search_pane = self.browser.find_element_by_id('search_pane')

        self.assertTrue(search_pane.is_displayed())

        # John sees a search field.
        search_field = self.browser.find_element_by_id('search_field')

        self.assertEqual(search_field.get_attribute('placeholder'), 'Name or email')

        # He enters the name 'Nina' into the search field and clicks the search button.
        # Nina does not exist, so the words 'No users found' appear on the screen.
        search_field.send_keys('Nina')

        search_button = self.browser.find_element_by_id('search_button')
        search_button.click()

        search_results = self.browser.find_element_by_id('search_results')

        self.wait_for(lambda: self.assertIn('No results found', search_results.text))

        # He enters the name 'Regina' into the search field and clicks the search button.
        # Regina does exist, so her profile appears on the screen.
        User.objects.create_user(
            first_name='Regina',
            last_name='Mcdonalid',
            email='regina.mcdonalid93@example.com',
            username='regina.mcdonalid93@example.com',
            password='password1'
        )

        search_field.clear()
        search_field.send_keys('Regina')

        search_button.click()

        self.wait_for(lambda: self.assertIn('Regina Mcdonalid', search_results.text))

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

        # He clicks the requests tab.
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

        # Regina is a user.
        User.objects.create_user(
            first_name='Regina',
            last_name='Mcdonalid',
            email='regina.mcdonalid93@example.com',
            username='regina.mcdonalid93@example.com',
            password='password1'
        )

        # John clicks the browse tab.
        browse_tab = self.browser.find_element_by_id('browse_tab')
        browse_tab.click()

        # The browse pane is revealed.
        browse_pane = self.browser.find_element_by_id('browse_pane')

        self.assertTrue(browse_pane.is_displayed())

        # John sees Regina's information.
        browse_results = self.browser.find_element_by_id('browse_results')

        self.wait_for(lambda: self.assertIn('Regina Mcdonalid', browse_results.text))

    def test_friends(self):
        # John is a logged-in user.
        self.create_pre_authenticated_session(
            first_name='John',
            last_name='Carney',
            email='john.carney@carneylabs.com',
            password='password1'
        )

        # John goes to the users page.
        self.browser.get(self.live_server_url + '/users/')

        # He clicks the friends tab.
        friends_tab = self.browser.find_element_by_id('friends_tab')
        friends_tab.click()

        # The friends pane is revealed.
        friends_pane = self.browser.find_element_by_id('friends_pane')

        self.assertTrue(friends_pane.is_displayed())