__author__ = 'jason.parent@carneylabs.com (Jason Parent)'

# Django imports...
from django.contrib.auth import get_user_model
from django.test import TestCase

# Local imports...
from ..models import Friendship

User = get_user_model()


class FriendshipModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='john.carney@carneylabs.com',
            email='john.carney@carneylabs.com',
            password='password1'
        )

        self.friend = User.objects.create_user(
            email='regina.mcdonalid93@example.com',
            username='regina.mcdonalid93@example.com',
            password='password1'
        )

    def test_non_friends_do_not_share_friendship(self):
        self.assertFalse(Friendship.user_has_friend(self.user, self.friend))
        self.assertFalse(Friendship.user_has_friend(self.friend, self.user))

    def test_friends_share_friendship(self):
        Friendship.objects.create(sender=self.user, receiver=self.friend, status='A')

        self.assertTrue(Friendship.user_has_friend(self.user, self.friend))
        self.assertTrue(Friendship.user_has_friend(self.friend, self.user))

    def test_added_friends_share_pending_friendship(self):
        friendship = Friendship.user_add_friend(self.user, self.friend)

        self.assertTrue(friendship.status, 'P')

    def test_friendship_abolished_when_sender_removes_friend(self):
        Friendship.objects.create(sender=self.user, receiver=self.friend, status='A')
        Friendship.user_remove_friend(self.user, self.friend)

        self.assertFalse(Friendship.user_has_friend(self.user, self.friend))
        self.assertFalse(Friendship.user_has_friend(self.friend, self.user))

    def test_friendship_abolished_when_receiver_removes_friend(self):
        Friendship.objects.create(sender=self.user, receiver=self.friend, status='A')
        Friendship.user_remove_friend(self.friend, self.user)

        self.assertFalse(Friendship.user_has_friend(self.user, self.friend))
        self.assertFalse(Friendship.user_has_friend(self.friend, self.user))

    def test_friends_in_friends_list(self):
        Friendship.objects.create(sender=self.user, receiver=self.friend, status='A')

        self.assertIn(self.friend, Friendship.user_list_friends(self.user))

    def test_friendship_has_accepted_status_when_accepted(self):
        friendship = Friendship.objects.create(sender=self.user, receiver=self.friend, status='P')
        friendship.accept()

        self.assertEqual(friendship.status, 'A')

    def test_friendship_has_rejected_status_when_rejected(self):
        friendship = Friendship.objects.create(sender=self.user, receiver=self.friend, status='P')
        friendship.reject()

        self.assertEqual(friendship.status, 'R')


class FriendshipQuerySetTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='john.carney@carneylabs.com',
            email='john.carney@carneylabs.com',
            password='password1'
        )

        self.regina = User.objects.create_user(
            email='regina.mcdonalid93@example.com',
            username='regina.mcdonalid93@example.com',
            password='password1'
        )

        self.brandon = User.objects.create_user(
            email='brandon.jacobs96@example.com',
            username='brandon.jacobs96@example.com',
            password='password1'
        )

        self.tim = User.objects.create_user(
            email='tim.johnson39@example.com',
            username='tim.johnson39@example.com',
            password='password1'
        )

        self.user_and_regina = Friendship.objects.create(sender=self.user, receiver=self.regina, status='A')
        self.user_and_brandon = Friendship.objects.create(sender=self.user, receiver=self.brandon, status='P')
        self.user_and_tim = Friendship.objects.create(sender=self.tim, receiver=self.user, status='P')

    def test_get_friendship(self):
        # User and Regina...
        self.assertEqual(Friendship.objects.get_friendship(self.user, self.regina), self.user_and_regina)
        self.assertEqual(Friendship.objects.get_friendship(self.regina, self.user), self.user_and_regina)

        # User and Brandon...
        self.assertEqual(Friendship.objects.get_friendship(self.user, self.brandon), self.user_and_brandon)
        self.assertEqual(Friendship.objects.get_friendship(self.brandon, self.user), self.user_and_brandon)

        # User and Tim...
        self.assertEqual(Friendship.objects.get_friendship(self.user, self.tim), self.user_and_tim)
        self.assertEqual(Friendship.objects.get_friendship(self.tim, self.user), self.user_and_tim)

    def test_get_friendships(self):
        friendships = Friendship.objects.get_friendships(self.user)

        self.assertListEqual([self.user_and_regina, self.user_and_brandon, self.user_and_tim], list(friendships))

    def test_pending(self):
        friendships = Friendship.objects.pending(self.user)

        self.assertListEqual([self.user_and_brandon, self.user_and_tim], list(friendships))

    def test_pending_sent(self):
        friendships = Friendship.objects.pending_sent(self.user)

        self.assertListEqual([self.user_and_brandon], list(friendships))

    def test_pending_received(self):
        friendships = Friendship.objects.pending_received(self.user)

        self.assertListEqual([self.user_and_tim], list(friendships))

    def test_current(self):
        friendships = Friendship.objects.current(self.user)

        self.assertListEqual([self.user_and_regina], list(friendships))