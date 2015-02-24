__author__ = 'jason.parent@carneylabs.com (Jason Parent)'

# Django imports...
from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY
from django.contrib.auth import SESSION_KEY
from django.contrib.auth import get_user_model
from django.contrib.sessions.backends.db import SessionStore
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    def handle(self, email, password, *args, **kwargs):
        session_key = create_pre_authenticated_session(email, password, *args, **kwargs)

        self.stdout.write(session_key)


def create_pre_authenticated_session(email, password, *args, **kwargs):
    user = User.objects.create_user(username=email, email=email, password=password, *args, **kwargs)

    session = SessionStore()
    session[SESSION_KEY] = user.pk
    session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
    session.save()

    return session.session_key