from django.test import TestCase
from django.urls import reverse

# Create your tests here.
class TestContacts(TestCase):

    def test_contacts_page(self):
        response = self.client.get(reverse('contacts:show_contacts'))
        self.assertEqual(response.status_code, 200)
