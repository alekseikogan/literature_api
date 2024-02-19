from unittest import TestCase

from books.wsgi import *
from store.models import Book
from store.serializers import BookSerializer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'books.settings')
import django
django.setup()


class BookSerializerTestCase(TestCase):

    def test_get_books(self):
        book1 = Book.objects.create(title='Book 1', price=10.99)
        book2 = Book.objects.create(title='Book 2', price=20.99)
        data = BookSerializer([book1, book2], many=True).data
        expected_data = [
            {
                'id': book1.id,
                'title': 'Book 1',
                'price': '10.99'
            },
            {
                'id': book2.id,
                'title': 'Book 2',
                'price': '20.99'
            }
        ]
        self.assertEqual(expected_data, data)
