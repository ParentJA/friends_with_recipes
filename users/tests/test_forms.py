__author__ = 'jason.parent@carneylabs.com (Jason Parent)'

# Django imports...
from django.test import TestCase

# Local imports...
from ..forms import ProfileForm


class ProfileFormTest(TestCase):
    def test_form_has_required_fields(self):
        form = ProfileForm()

        self.assertIn('id="id_photo"', form.as_p())