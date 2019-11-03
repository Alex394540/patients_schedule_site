from django.test import TestCase
from django.urls import reverse
from .models import News


# Create your tests here.
class TestNews(TestCase):

    def test_news_page(self):
        response = self.client.get(reverse('news:show_news'))
        self.assertEqual(response.status_code, 200)
