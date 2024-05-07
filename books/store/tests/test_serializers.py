from unittest import TestCase
from books.store.models import UserBookRelation
from django.db.models import Case, Count, When, Avg
from django.contrib.auth import get_user_model

from books.wsgi import *
from store.models import Book
from store.serializers import BookSerializer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'books.settings')
import django
django.setup()


User = get_user_model()

class BookSerializerTestCase(TestCase):

    def setUp(self):
        user1 = User.objects.create(username='user1')
        user2 = User.objects.create(username='user2')
        user3 = User.objects.create(username='user3')
        self.book1 = Book.objects.create(title='Book 1', price=10.99, author='Author 1')
        self.book2 = Book.objects.create(title='Book 2', price=20.99, author='Author 2')
        self.book3 = Book.objects.create(title='Book 3', price=30.99, author='Author 3')

        UserBookRelation.objects.create(user=user1, book=self.book1, like=True, rate=5)
        UserBookRelation.objects.create(user=user2, book=self.book1, like=True, rate=5)
        UserBookRelation.objects.create(user=user3, book=self.book1, like=True, rate=4)

        UserBookRelation.objects.create(user=user1, book=self.book2, like=True, rate=3)
        UserBookRelation.objects.create(user=user2, book=self.book2, like=True, rate=4)
        UserBookRelation.objects.create(user=user3, book=self.book2, like=False)

    def test_serializer_get(self):
        books = Book.objects.all().annotate(
            annotated_likes=Count(
                Case(
                    When(userbookrelation__like=True, then=1))),
            rating=Avg('userbookrelation__rate')
        ).order_by('id')
        data = BookSerializer(books, many=True).data
        expected_data = [
            { 
                'id': self.book1.id,
                'title': 'Book 1',
                'price': '10.99',
                'author': 'Author 1',
                'likes_count': 0,
                'rating': 0,
            },
            {
                'id': self.book2.id,
                'title': 'Book 2',
                'price': '20.99',
                'author': 'Author 2',
                'likes_count': 0,
                'rating': 0,
            },
            {
                'id': self.book3.id,
                'title': 'Book 3',
                'price': '30.99',
                'author': 'Author 3',
                'likes_count': 0,
                'rating': 0,
            }
        ]
        self.assertEqual(expected_data, data)
