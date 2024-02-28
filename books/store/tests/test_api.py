# from books.wsgi import *
import os
from decimal import Decimal

from books.store.serializers import UserBookRelationSerializer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'books.settings')
import django
django.setup()

from operator import itemgetter

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.utils import json

from store.models import Book
from store.serializers import BookSerializer



from rest_framework.test import APITestCase

from django.urls import reverse


class BooksApiTestCase(APITestCase):

    def setUp(self):

        self.user = User.objects.create(username='testuser')
        self.book1 = Book.objects.create(title='Book 1', price=10.99, author='Author 1', owner=self.user)
        self.book2 = Book.objects.create(title='Book 2', price=20.99, author='Author 2', owner=self.user)
        self.book3 = Book.objects.create(title='Book 3 Author 1', price=30.99, author='Author 3', owner=self.user)

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

    # def test_ordering(self):
    #     """Проверка сортировки"""
    #
    #     url = reverse('book-list')
    #     response = self.client.get(url, data={'ordering': '-title'})
    #     serializer_data = BookSerializer([self.book1, self.book2, self.book3], many=True)
    #     serializer_data_sort = sorted(serializer_data.to_representation(serializer_data.data), key=itemgetter('title'))
    #     self.assertEqual(serializer_data_sort, response.data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create(self):
        """Проверка создания"""

        self.assertEqual(3, Book.objects.all().count())
        url = reverse('book-list')
        data = {
            'title': 'Book 4',
            'price': 40.99,
            'author': 'Author 4'
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(4, Book.objects.all().count())
        self.assertEqual(self.user, Book.objects.last().owner)

    def test_update(self):
        """Проверка обновления записи"""

        url = reverse('book-detail', args=(self.book1.id,))
        data = {
            'title': self.book1.title,
            'price': 15.99,
            'author': self.book1.author
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.book1.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_not_owner(self):
        """Проверка обновления записи не владельцем"""

        self.user2 = User.objects.create(username='testuser2')
        url = reverse('book-detail', args=(self.book1.id,))
        data = {
            'title': self.book1.title,
            'price': 15.99,
            'author': self.book1.author
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.book1.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.book1.price, round(Decimal(10.99), 2))

    def test_update_not_owner_but_staff(self):
        """Проверка обновления записи админом"""

        self.user2 = User.objects.create(username='testuser2',
                                         is_staff=True)
        url = reverse('book-detail', args=(self.book1.id,))
        data = {
            'title': self.book1.title,
            'price': 15.99,
            'author': self.book1.author
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.book1.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.book1.price, round(Decimal(15.99), 2))

    def test_delete(self):
        """Проверка удаления записи"""
        pass


class BookRealtionTestCase(APITestCase):

    def setUp(self) -> None:
        
        self.user = User.objects.create(username='testuser')
        self.user2 = User.objects.create(username='testuser2')
        self.book1 = Book.objects.create(title='Book 1', price=10.99, author='Author 1', owner=self.user)
        self.book2 = Book.objects.create(title='Book 2', price=20.99, author='Author 2', owner=self.user)
        self.book3 = Book.objects.create(title='Book 3 Author 1', price=30.99, author='Author 3', owner=self.user)

    def test_get(self):
        url = reverse('userbookrelation-detail', args=(self.book1.id,))
        data = {
            'like': True,
        }
        self.client.force_login(self.user)
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.book1.refresh_from_db()
        self.assertTrue(self.book1.like)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
