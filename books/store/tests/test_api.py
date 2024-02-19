from books.wsgi import *
from store.models import Book
from store.serializers import BookSerializer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'books.settings')
import django
django.setup()

from rest_framework.test import APITestCase

from django.urls import reverse


class BooksApiTestCase(APITestCase):

    def test_get_books(self):
        book1 = Book.objects.create(title='Book 1', price=10.99)
        book2 = Book.objects.create(title='Book 2', price=20.99)
        url = reverse('book-list')
        response = self.client.get(url)
        serializer_data = BookSerializer([book1, book2], many=True).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(response.status_code, 200)
