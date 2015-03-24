__author__ = 'jason.parent@carneylabs.com (Jason Parent)'

# Third-party imports...
from mock import Mock
from mock import patch

# Django imports...
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test.client import RequestFactory
from django.test import Client
from django.test import TestCase

# Local imports...
from ..models import Friendship
from ..views import home_view

User = get_user_model()


class HomeViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/users/')
        self.request.user = User.objects.create_user(
            username='john.carney@carneylabs.com',
            email='john.carney@carneylabs.com',
            password='password1'
        )

    def test_home_view_renders_home_template(self):
        response = home_view(self.request)

        self.assertTemplateUsed(response, 'users/home.html')


class FriendshipTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            first_name='John',
            last_name='Carney',
            username='john.carney@carneylabs.com',
            email='john.carney@carneylabs.com',
            password='password1'
        )

        self.client = Client()
        self.client.login(username='john.carney@carneylabs.com', password='password1')


class ListViewTest(FriendshipTest):
    def test_list_view_renders_list_template(self):
        response = self.client.get('/users/list/')

        self.assertTemplateUsed(response, 'users/list.html')

    def test_list_view_returns_empty_list_for_invalid_search(self):
        response = self.client.get('/users/list/?search=nonexistent')

        self.assertListEqual(list(response.context['users']), [])

    def test_list_view_returns_valid_list_for_valid_search(self):
        regina = User.objects.create_user(
            username='regina.mcdonalid93@example.com',
            email='regina.mcdonalid93@example.com',
            password='password1'
        )

        User.objects.create_user(
            username='travis.mills57@example.com',
            email='travis.mills57@example.com',
            password='password1'
        )

        response = self.client.get('/users/list/?search=regina')

        self.assertIn(regina, response.context['users'])

    def test_list_view_returns_all_users_except_request_user_on_empty_search(self):
        regina = User.objects.create_user(
            username='regina.mcdonalid93@example.com',
            email='regina.mcdonalid93@example.com',
            password='password1'
        )

        travis = User.objects.create_user(
            username='travis.mills57@example.com',
            email='travis.mills57@example.com',
            password='password1'
        )

        response = self.client.get('/users/list/')

        self.assertIn(regina, response.context['users'])
        self.assertIn(travis, response.context['users'])


class RequestsViewTest(FriendshipTest):
    def test_requests_view_renders_requests_template(self):
        response = self.client.get('/users/requests/')

        self.assertTemplateUsed(response, 'users/requests.html')

    @patch('users.views.Friendship.user_list_friends')
    def test_requests_view_returns_pending_received_friendships(self, mock_user_list_friends):
        mock_friend = Mock(pk=1)
        mock_user_list_friends.return_value = [mock_friend]

        response = self.client.get('/users/requests/')

        self.assertListEqual([mock_friend], response.context['users'])


class FriendsViewTest(FriendshipTest):
    def test_friends_view_renders_friends_template(self):
        response = self.client.get('/users/friends/')

        self.assertTemplateUsed(response, 'users/friends.html')

    @patch('users.views.Friendship.user_list_friends')
    def test_friends_view_returns_current_friendships(self, mock_user_list_friends):
        mock_friend = Mock()
        mock_user_list_friends.return_value = [mock_friend]

        response = self.client.get('/users/friends/')

        self.assertListEqual([mock_friend], response.context['users'])


class AddViewTest(FriendshipTest):
    def test_add_view_redirects_home(self):
        regina = User.objects.create_user(
            username='regina.mcdonalid93@example.com',
            email='regina.mcdonalid93@example.com',
            password='password1'
        )

        response = self.client.get(reverse('users:add', args=[regina.pk]))

        self.assertRedirects(response, '/users/')

    def test_add_view_raises_404_for_invalid_user(self):
        response = self.client.get(reverse('users:add', args=[1000]))

        self.assertEqual(response.status_code, 404)

    @patch('users.views.Friendship')
    def test_friend_added_for_valid_user(self, mock_friendship):
        mock_friendship.objects.get_friendship.return_value = Mock()
        mock_friendship.user_add_friend.return_value = None

        regina = User.objects.create_user(
            username='regina.mcdonalid93@example.com',
            email='regina.mcdonalid93@example.com',
            password='password1'
        )

        self.client.get(reverse('users:add', args=[regina.pk]))

        mock_friendship.user_add_friend.assert_called_once_with(self.user, regina)


class AcceptViewTest(FriendshipTest):
    @patch('users.views.Friendship')
    def test_accept_view_redirects_home(self, mock_friendship):
        mock_friendship.objects.get_friendship.return_value = Mock()

        regina = User.objects.create_user(
            username='regina.mcdonalid93@example.com',
            email='regina.mcdonalid93@example.com',
            password='password1'
        )

        response = self.client.get(reverse('users:accept', args=[regina.pk]))

        self.assertRedirects(response, '/users/')

    def test_accept_view_raises_404_for_invalid_user(self):
        response = self.client.get(reverse('users:accept', args=[1000]))

        self.assertEqual(response.status_code, 404)

    @patch('users.views.Friendship')
    def test_friendship_accepted_for_valid_user(self, mock_friendship):
        mock_friendship_instance = mock_friendship.objects.get_friendship
        mock_friendship_instance.return_value.accept.return_value = None

        regina = User.objects.create_user(
            username='regina.mcdonalid93@example.com',
            email='regina.mcdonalid93@example.com',
            password='password1'
        )

        self.client.get(reverse('users:accept', args=[regina.pk]))

        mock_friendship_instance.assert_called_once_with(self.user, regina)

        self.assertTrue(mock_friendship_instance.return_value.accept.called)


class RejectViewTest(FriendshipTest):
    @patch('users.views.Friendship')
    def test_reject_view_redirects_home(self, mock_friendship):
        mock_friendship.objects.get_friendship.return_value = Mock()

        regina = User.objects.create_user(
            username='regina.mcdonalid93@example.com',
            email='regina.mcdonalid93@example.com',
            password='password1'
        )

        response = self.client.get(reverse('users:reject', args=[regina.pk]))

        self.assertRedirects(response, '/users/')

    def test_reject_view_raises_404_for_invalid_user(self):
        response = self.client.get(reverse('users:reject', args=[1000]))

        self.assertEqual(response.status_code, 404)

    @patch('users.views.Friendship')
    def test_friendship_rejected_for_valid_user(self, mock_friendship):
        mock_friendship_instance = mock_friendship.objects.get_friendship
        mock_friendship_instance.return_value.reject.return_value = None

        regina = User.objects.create_user(
            username='regina.mcdonalid93@example.com',
            email='regina.mcdonalid93@example.com',
            password='password1'
        )

        self.client.get(reverse('users:reject', args=[regina.pk]))

        mock_friendship_instance.assert_called_once_with(self.user, regina)

        self.assertTrue(mock_friendship_instance.return_value.reject.called)


class FeedViewTest(FriendshipTest):
    def setUp(self):
        super(FeedViewTest, self).setUp()

        self.regina = User.objects.create_user(
            first_name='Regina',
            last_name='McDonald',
            username='regina.mcdonalid93@example.com',
            email='regina.mcdonalid93@example.com',
            password='password1'
        )

        self.friendship = Friendship.user_add_friend(self.user, friend=self.regina)
        self.friendship.accept()

    def test_feed_view_renders_feed_template(self):
        response = self.client.get('/users/feed/')

        self.assertTemplateUsed(response, 'users/feed.html')

    def test_feed_view_returns_user_events(self):
        response = self.client.get('/users/feed/')

        self.assertListEqual(response.context['events'], [{
            'heading': '%s added %s as a friend' % (
                self.friendship.sender.first_name,
                self.friendship.receiver.first_name
            ),
            'date': self.friendship.created,
            'first_subject': self.friendship.sender,
            'indirect_object': self.friendship.receiver
        }, {
            'heading': '%s %s %s\'s friendship' % (
                self.friendship.receiver.first_name,
                self.friendship.get_status_display(),
                self.friendship.sender.first_name
            ),
            'date': self.friendship.updated,
            'first_subject': self.friendship.receiver,
            'indirect_object': self.friendship.sender
        }])

    def test_feed_view_returns_user_events_in_correct_order(self):
        response = self.client.get('/users/feed/')

        self.assertListEqual(
            [e.get('date') for e in response.context['events']],
            [self.friendship.created, self.friendship.updated]
        )