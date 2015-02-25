__author__ = 'jason.parent@carneylabs.com (Jason Parent)'

# Django imports...
from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class UserModelTest(TestCase):
    def test_user_unicode_representation(self):
        user = User.objects.create_user(
            first_name='John',
            last_name='Carney',
            username='john.carney@carneylabs.com',
            email='john.carney@carneylabs.com',
            password='password'
        )

        self.assertEqual(unicode(user), user.get_full_name())
        self.assertEqual(unicode(user), 'John Carney')