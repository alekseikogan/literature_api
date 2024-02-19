from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Цена')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'books'
        ordering = ('title',)
        verbose_name = 'Книги'
        verbose_name_plural = 'Книги'
