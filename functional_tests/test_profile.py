__author__ = 'jason.parent@carneylabs.com (Jason Parent)'

# Local imports...
from .base import FunctionalTest


class ProfileTest(FunctionalTest):
    def test_profile_view(self):
        # John is a logged-in user.
        self.create_pre_authenticated_session(
            first_name='John',
            last_name='Carney',
            email='john.carney@carneylabs.com',
            password='password1'
        )

        # John goes to the profile page.
        self.browser.get(self.live_server_url + '/profile/')

        # He notices a user image and five icons that display profile information when he clicks
        # or moves the cursor over them.
        user = self.browser.find_element_by_id('user')
        envelope = self.browser.find_element_by_id('envelope')
        calendar = self.browser.find_element_by_id('calendar')
        marker = self.browser.find_element_by_id('marker')
        phone = self.browser.find_element_by_id('phone')

        # He clicks the first icon and sees his full name.
        user.click()
        user_display = self.browser.find_element_by_css_selector("#user-display h4")

        self.assertEqual(user_display.text, 'John Carney')

        # He clicks the second icon and sees his email address.
        envelope.click()
        envelope_display = self.browser.find_element_by_css_selector('#envelope-display h4')

        self.assertEqual(envelope_display.text, 'john.carney@carneylabs.com')

        # He clicks the third icon and sees 'None'.
        calendar.click()
        calendar_display = self.browser.find_element_by_css_selector('#calendar-display h4')

        self.assertEqual(calendar_display.text, 'None')

        # He clicks the fourth icon and sees 'None'.
        marker.click()
        marker_display = self.browser.find_element_by_css_selector('#marker-display h4')

        self.assertEqual(marker_display.text, 'None')

        # He clicks the fifth icon and sees 'None'.
        phone.click()
        phone_display = self.browser.find_element_by_css_selector('#phone-display h4')

        self.assertEqual(phone_display.text, 'None')

    def test_profile_edit(self):
        # John is a logged-in user.
        self.create_pre_authenticated_session(
            first_name='John',
            last_name='Carney',
            email='john.carney@carneylabs.com',
            password='password1'
        )

        # John goes to the profile page.
        self.browser.get(self.live_server_url + '/profile/')

        # He notices a link with a user image and he clicks it.
        edit = self.browser.find_element_by_id('edit-button')
        edit.click()

        # The page refreshes and John sees a form that allows him to edit his profile.
        # The form has photo, data of birth, address, and phone number fields.
        # There is also a button that says 'Submit'.
        # John adds his data and clicks the 'Submit' button.
        # TODO: Not sure how to test this...
        self.browser.find_element_by_id('id_photo')
        self.browser.find_element_by_id('id_date_of_birth').send_keys('06/02/1979')
        self.browser.find_element_by_id('id_address').send_keys('100 North Pitt Street')
        self.browser.find_element_by_id('id_phone_number').send_keys('(913) 149-4498')

        submit = self.browser.find_element_by_id('submit_button')

        self.assertEqual(submit.text, 'Submit')

        submit.click()

        # The page refreshes again and John notices that his data has changed.
        calendar = self.browser.find_element_by_id('calendar')
        marker = self.browser.find_element_by_id('marker')
        phone = self.browser.find_element_by_id('phone')

        calendar.click()
        calendar_display = self.browser.find_element_by_css_selector('#calendar-display h4')

        self.assertEqual(calendar_display.text, 'June 2, 1979')

        marker.click()
        marker_display = self.browser.find_element_by_css_selector('#marker-display h4')

        self.assertEqual(marker_display.text, '100 North Pitt Street')

        phone.click()
        phone_display = self.browser.find_element_by_css_selector('#phone-display h4')

        self.assertEqual(phone_display.text, '913-149-4498')