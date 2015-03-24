__author__ = 'jason.parent@carneylabs.com (Jason Parent)'

# Django imports...
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models import QuerySet
from django.utils import timezone

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL')

FRIENDSHIP_STATUS = (
    ('P', 'pending'),
    ('A', 'accepted'),
    ('R', 'rejected'),
)


class FriendshipQuerySet(QuerySet):
    def get_friendship(self, user, friend):
        """Gets a friendship between the user and the specified friend, if one exists."""
        query = Q(
            Q(sender=user, receiver=friend) |
            Q(sender=friend, receiver=user)
        )

        try:
            return self.get(query)
        except Friendship.DoesNotExist:
            return None

    def get_friendships(self, user, status=None, sent=True, received=True):
        """
        Get all friendships associated with the user according to the status and whether the user
        sent and/or received the friendship request.
        """
        query = Q()

        if sent:
            query = Q(sender=user)

        if received:
            query |= Q(receiver=user)

        friendships = self.filter(query)

        if status:
            friendships = friendships.filter(status=status)

        return friendships.order_by('updated')

    def pending(self, user):
        """Get all pending friendships associated with the user."""
        return self.get_friendships(user, 'P')

    def pending_sent(self, user):
        """Get all pending friendships that were sent by the user."""
        return self.get_friendships(user, 'P', sent=True, received=False)

    def pending_received(self, user):
        """Get all pending friendships that were received by the user."""
        return self.get_friendships(user, 'P', sent=False, received=True)

    def current(self, user):
        """Get all current (accepted) friendships associated with the user."""
        return self.get_friendships(user, 'A')


class Friendship(models.Model):
    sender = models.ForeignKey(AUTH_USER_MODEL, related_name='friendships_by_sender')
    receiver = models.ForeignKey(AUTH_USER_MODEL, related_name='friendships_by_receiver')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=FRIENDSHIP_STATUS, default='P')

    objects = FriendshipQuerySet.as_manager()

    class Meta:
        unique_together = ('sender', 'receiver')

    @staticmethod
    def user_has_friend(user, friend):
        """Checks whether the user is part of a friendship with the specified friend."""
        return Friendship.objects.get_friendship(user, friend) is not None

    @staticmethod
    def user_add_friend(user, friend):
        """Creates a pending friendship between the user and the specified friend."""
        if friend == user or Friendship.user_has_friend(user, friend):
            return None

        return Friendship.objects.create(sender=user, receiver=friend)

    @staticmethod
    def user_remove_friend(user, friend):
        """Removes a friend, if a friendship exists between the user and the specified friend."""
        if friend == user:
            return None

        friendship = Friendship.objects.get_friendship(user, friend)

        if not friendship:
            return None

        friendship.delete()

        return friendship

    @staticmethod
    def user_list_friends(user, friendships=None):
        """Gets a list of friends from the specified friendships."""
        if friendships is None:
            friendships = Friendship.objects.current(user)

        # Extract non-self friends from friendships...
        return map((lambda f: f.sender if f.receiver == user else f.receiver), friendships)

    def __unicode__(self):
        return '%s to %s (%s)' % (
            self.sender.first_name,
            self.receiver.first_name,
            self.get_status_display()
        )

    def accept(self):
        """Accepts a pending friendship."""
        if self.status != 'P':
            return None

        self.status = 'A'
        self.updated = timezone.now()
        self.save()

    def reject(self):
        """Rejects a pending friendship."""
        if self.status != 'P':
            return None

        self.status = 'R'
        self.updated = timezone.now()
        self.save()