from operator import itemgetter

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
        self.book3 = Book.objects.create(title='Book 3 Author 1', price=30.99, author='Author 3')

    def test_get_books(self):
        """Проверка получения списка книг"""

        url = reverse('book-list')
        response = self.client.get(url)
        serializer_data = BookSerializer([self.book1, self.book2, self.book3], many=True).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter(self):
        """Проверка фильтраци"""

        url = reverse('book-list')
        response = self.client.get(url, data={'search': 'Author 1'})
        serializer_data = BookSerializer([self.book1, self.book3], many=True).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ordering(self):
        """Проверка сортировки"""

        url = reverse('book-list')
        response = self.client.get(url, data={'ordering': '-title'})
        serializer_data = BookSerializer([self.book3, self.book2, self.book1], many=True)
        serializer_data1 = sorted(serializer_data.to_representation(serializer_data.data), key=itemgetter('title'))
        self.assertEqual(serializer_data1, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
