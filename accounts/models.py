__author__ = 'jason.parent@carneylabs.com (Jason Parent)'

# Django imports...
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    photo = models.ImageField(upload_to='photos', default='photos/no-image.jpg', blank=True, null=True)

    def __unicode__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)

    @property
    def photo_url(self):
        try:
            return self.photo.url
        except ValueError:
            return None