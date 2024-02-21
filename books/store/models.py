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
        related_name='books',
        verbose_name='Владелец')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'books'
        ordering = ('title',)
        verbose_name = 'Книги'
        verbose_name_plural = 'Книги'
