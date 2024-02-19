import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'books.settings')
import django
django.setup()

from rest_framework.test import APITestCase

from django.urls import reverse


class BooksApiTestCase(APITestCase):

    def test_get_books(self):
        url = reverse('book-list')
        print(f'url: {url}')
        response = self.client.get(url)
        print(f'response: {response}')
