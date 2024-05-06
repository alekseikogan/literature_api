from unittest import TestCase

from books.wsgi import *
from store.models import Book
from store.serializers import BookSerializer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'books.settings')
import django
django.setup()


class BookSerializerTestCase(TestCase):

    def setUp(self):
        self.book1 = Book.objects.create(title='Book 1', price=10.99, author='Author 1')
        self.book2 = Book.objects.create(title='Book 2', price=20.99, author='Author 2')
        self.book3 = Book.objects.create(title='Book 3', price=30.99, author='Author 3')

    def test_serializer_get(self):
        books = Book.objects.all()
        data = BookSerializer([self.book1, self.book2, self.book3], many=True).data
        expected_data = [
            {
                'id': self.book1.id,
                'title': 'Book 1',
                'price': '10.99',
                'author': 'Author 1',
                'likes_count': 0,
            },
            {
                'id': self.book2.id,
                'title': 'Book 2',
                'price': '20.99',
                'author': 'Author 2',
                'likes_count': 0,
            },
            {
                'id': self.book3.id,
                'title': 'Book 3',
                'price': '30.99',
                'author': 'Author 3',
                'likes_count': 0,
            }
        ]
        self.assertEqual(expected_data, data)
