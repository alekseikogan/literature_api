from rest_framework import status

from books.wsgi import *
from store.models import Book
from store.serializers import BookSerializer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'books.settings')
import django
django.setup()

from rest_framework.test import APITestCase

from django.urls import reverse


class BooksApiTestCase(APITestCase):

    def setUp(self):
        self.book1 = Book.objects.create(title='Book 1', price=10.99, author='Author 1')
        self.book2 = Book.objects.create(title='Book 2', price=20.99, author='Author 2')
        self.book3 = Book.objects.create(title='Book 3', price=30.99, author='Author 3')

    def test_get_books(self):
        url = reverse('book-list')
        response = self.client.get(url)
        serializer_data = BookSerializer([self.book1, self.book2, self.book3], many=True).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
