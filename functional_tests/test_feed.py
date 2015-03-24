__author__ = 'jason.parent@carneylabs.com (Jason Parent)'

# Django imports...
from django.conf import settings
from django.contrib.auth import get_user_model
from django.template.defaulttags import date

# Local imports...
from .base import FunctionalTest
from users.models import Friendship

User = get_user_model()


class FeedTest(FunctionalTest):
    def test_user_without_friends_sees_empty_feed(self):
        # John is a logged-in user.
        self.create_pre_authenticated_session(
            first_name='John',
            last_name='Carney',
            email='john.carney@carneylabs.com',
            password='password1'
        )

        # He visits the homepage.
        self.browser.get(self.live_server_url + '/users/feed/')

        # John sees a message that reads "Nothing notable has happened. Try making some friends."
        container = self.browser.find_element_by_css_selector('body > div.container')

        self.assertEqual(container.text, 'Nothing notable has happened. Try making some friends.')

    def test_user_with_friends_sees_friendship_events_in_feed(self):
        # John is a logged-in user.
        self.create_pre_authenticated_session(
            first_name='John',
            last_name='Carney',
            email='john.carney@carneylabs.com',
            password='password1'
        )

        # He has sent a friend request to Regina, who has accepted the request.
        john = User.objects.get(username='john.carney@carneylabs.com')
        regina = User.objects.create_user(
            first_name='Regina',
            last_name='Mcdonalid',
            email='regina.mcdonalid93@example.com',
            username='regina.mcdonalid93@example.com',
            password='password1'
        )

        friendship = Friendship.user_add_friend(john, friend=regina)
        friendship.accept()

        # He visits the homepage.
        self.browser.get(self.live_server_url + '/users/feed/')

        # He sees a list of events.
        event_list = self.browser.find_element_by_class_name('media-list')
        events = event_list.find_elements_by_class_name('media')

        # John sees a container describing the event of his friendship request to Regina.
        # The container has a label that reads "John added Regina as a friend" and there
        # is also a description with the date the friendship was created.
        event_1st = events[0]
        event_body = event_1st.find_element_by_class_name('media-body')

        self.assertIn('John added Regina as a friend', event_body.text)
        self.assertIn(date(friendship.created, getattr(settings, 'SHORT_DATE_FORMAT')), event_body.text)

        # He also sees a container describing the event of Regina accepting his friendship request.
        # The container has a label that reads "Regina accepted John's friendship" and there
        # is also a description with the date the friendship was updated.
        event_2nd = events[1]
        event_body = event_2nd.find_element_by_class_name('media-body')

        self.assertIn('Regina accepted John\'s friendship', event_body.text)
        self.assertIn(date(friendship.updated, getattr(settings, 'SHORT_DATE_FORMAT')), event_body.text)