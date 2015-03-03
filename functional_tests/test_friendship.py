__author__ = 'jason.parent@carneylabs.com (Jason Parent)'

# Third-party imports...
from selenium.webdriver.firefox.webdriver import WebDriver

# Django imports...
from django.contrib.auth import get_user_model

# Local imports...
from .base import FunctionalTest

User = get_user_model()


def quit_if_possible(browser):
    try:
        browser.quit()
    except:
        pass


class FriendshipTest(FunctionalTest):
    def test_accept_friendship(self):
        # John is a logged-in user.
        self.create_pre_authenticated_session(
            first_name='John',
            last_name='Carney',
            email='john.carney@carneylabs.com',
            password='password1'
        )

        john_browser = self.browser

        self.addCleanup(lambda: quit_if_possible(john_browser))

        # Another user, Regina, is also on the Friends website.
        regina_browser = WebDriver()

        self.addCleanup(lambda: quit_if_possible(regina_browser))
        self.browser = regina_browser
        self.create_pre_authenticated_session(
            first_name='Regina',
            last_name='Mcdonalid',
            email='regina.mcdonalid93@example.com',
            password='password1'
        )

        self.browser = john_browser

        # John goes to the users page.
        self.browser.get(self.live_server_url + '/users/')

        # John clicks the browse tab.
        browse_tab = self.browser.find_element_by_id('browse_tab')
        browse_tab.click()

        # He sees Regina's information.
        browse_results = self.browser.find_element_by_id('browse_results')

        self.wait_for(lambda: self.assertIn('Regina Mcdonalid', browse_results.text))

        # He sees a button below her name that says 'Add friend' and he clicks it.
        regina_box = self.browser.find_element_by_class_name('media')
        add_button = regina_box.find_element_by_class_name('add')

        self.assertEqual(add_button.text, 'Add friend')

        add_button.click()

        # Regina goes to the users page.
        self.browser = regina_browser
        self.browser.get(self.live_server_url + '/users/')

        # She clicks the requests tab.
        requests_tab = self.browser.find_element_by_id('requests_tab')
        requests_tab.click()

        # She sees John's information.
        requests_results = self.browser.find_element_by_id('requests_results')

        self.wait_for(lambda: self.assertIn('John Carney', requests_results.text))

        # She sees a button that says 'Accept' and she clicks it.
        john_box = self.browser.find_element_by_class_name('media')
        accept_button = john_box.find_element_by_class_name('accept')

        self.assertEqual(accept_button.text, 'Accept')

        accept_button.click()

        # The page refreshes and she clicks on the friends tab.
        friends_tab = self.browser.find_element_by_id('friends_tab')
        friends_tab.click()

        # She sees John's information.
        friends_results = self.browser.find_element_by_id('friends_results')

        self.wait_for(lambda: self.assertIn('John Carney', friends_results.text))

        # John goes to the users page.
        self.browser = john_browser
        self.browser.get(self.live_server_url + '/users/')

        # He clicks on the friends tab.
        friends_tab = self.browser.find_element_by_id('friends_tab')
        friends_tab.click()

        # He sees that Regina is now his friend.
        friends_results = self.browser.find_element_by_id('friends_results')

        self.wait_for(lambda: self.assertIn('Regina Mcdonalid', friends_results.text))

    def test_reject_friendship(self):
        # John is a logged-in user.
        self.create_pre_authenticated_session(
            first_name='John',
            last_name='Carney',
            email='john.carney@carneylabs.com',
            password='password1'
        )

        john_browser = self.browser

        self.addCleanup(lambda: quit_if_possible(john_browser))

        # Another user, Regina, is also on the Friends website.
        regina_browser = WebDriver()

        self.addCleanup(lambda: quit_if_possible(regina_browser))
        self.browser = regina_browser
        self.create_pre_authenticated_session(
            first_name='Regina',
            last_name='Mcdonalid',
            email='regina.mcdonalid93@example.com',
            password='password1'
        )

        self.browser = john_browser

        # John goes to the users page.
        self.browser.get(self.live_server_url + '/users/')

        # John clicks the browse tab.
        browse_tab = self.browser.find_element_by_id('browse_tab')
        browse_tab.click()

        # He sees Regina's information.
        browse_results = self.browser.find_element_by_id('browse_results')

        self.wait_for(lambda: self.assertIn('Regina Mcdonalid', browse_results.text))

        # He sees a button below her name that says 'Add friend' and he clicks it.
        regina_box = self.browser.find_element_by_class_name('media')
        add_button = regina_box.find_element_by_class_name('add')

        self.assertEqual(add_button.text, 'Add friend')

        add_button.click()

        # Regina goes to the users page.
        self.browser = regina_browser
        self.browser.get(self.live_server_url + '/users/')

        # She clicks the requests tab.
        requests_tab = self.browser.find_element_by_id('requests_tab')
        requests_tab.click()

        # She sees John's information.
        requests_results = self.browser.find_element_by_id('requests_results')

        self.wait_for(lambda: self.assertIn('John Carney', requests_results.text))

        # She sees a button that says 'Reject' and she clicks it.
        john_box = self.browser.find_element_by_class_name('media')
        reject_button = john_box.find_element_by_class_name('reject')

        self.assertEqual(reject_button.text, 'Reject')

        reject_button.click()

        # The page refreshes and she clicks on the requests tab.
        requests_tab = self.browser.find_element_by_id('requests_tab')
        requests_tab.click()

        # John's information is gone.
        requests_results = self.browser.find_element_by_id('requests_results')

        self.wait_for(lambda: self.assertNotIn('John Carney', requests_results.text))

        # John goes to the users page.
        self.browser = john_browser
        self.browser.get(self.live_server_url + '/users/')

        # He clicks on the friends tab.
        friends_tab = self.browser.find_element_by_id('friends_tab')
        friends_tab.click()

        # He sees that Regina is not his friend.
        friends_results = self.browser.find_element_by_id('friends_results')

        self.wait_for(lambda: self.assertNotIn('Regina Mcdonalid', friends_results.text))