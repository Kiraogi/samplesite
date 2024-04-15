from django.db import models


class Bb(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название товара')
    content = models.TextField(verbose_name='Описание товара')
    price = models.FloatField(verbose_name='Цена товара')
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')

