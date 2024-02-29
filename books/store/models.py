from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Book(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Цена')
    author = models.CharField(max_length=255, verbose_name='Автор', default='Неизвестен')
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='my_books',
        verbose_name='Владелец')
    readers = models.ManyToManyField(
        User,
        through='UserBookRelation',
        related_name='books')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'books'
        ordering = ('title',)
        verbose_name = 'Книги'
        verbose_name_plural = 'Книги'


class UserBookRelation(models.Model):

    RATE_CHOISES = (
        (1, 'Bad'),
        (2, 'Fine'),
        (3, 'Good'),
        (4, 'Amazing'),
        (5, 'Incredible')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    in_bookmarks = models.BooleanField(default=False)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOISES, null=True)

    def __str__(self) -> str:
        return f'{self.user.username}|{self.book}|{self.rate}'
