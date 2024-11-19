from django.db import models
from django.contrib.auth.models import AbstractUser
from .utilities import get_timestamp_path

class Bb(models.Model):
    rubric = models.ForeingnKey(SubRubric, on_delete=models.PROTECT, verbose_name='Рубрика')
    title = models.CharField(max_length=50, verbose_name='Название товара')
    content = models.TextField(verbose_name='Описание товара')
    price = models.FloatField(default=0, verbose_name='Цена товара')
    contacts = models.TextField(verbose_name='Контакты')
    image = models.ImageField(blank=True, upload_to=get_timestamp_path, verbose_name='Изображение')
    author = models.ForeignKey(AdvUser, on_delete=models.CASCADE, verbose_name='Автор объявления')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Выводить в списке?')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')

def delete(self, *args, **kwargs):
    for ai in self.additionalimage_set.all():
        ai.delete()
    super().delete(*args, **kwargs)

class Meta:
    verbose_name_plural = 'Объявления'
    verbose_name = 'Объявление'
    ordering = ['-created_at']

class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True, verbose_name='Порядок')
    order = models.SmallIntegerField(default=0, db_index=True, verbose_name='Порядок')
    super_rubric = models.ForeignKey('SuperRubric', on_delete=models.PROTECT, null=True,
                                     blank=True, verbose_name='Надрубрика')


class SuperRubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=True)


class SuperRubric(Rubric):
    object = SuperRubricManager()

    def __str__(self):
        return self.name

    class Meta:
        proxy = True
        ordering = ['order', 'name']
        verbose_name = 'Надрубрика'
        verbose_name_plural = 'Надрубрики'


class SubRubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=False)


class SubRubric(Rubric):
    object = SubRubricManager()

    def __str__(self):
        return '%s - %s' % (self.super_rubric.name, self.name)

    class Meta:
        proxy = True
        ordering = ['super_rubric__order', 'super_rubric__name', 'order', 'name']
        verbose_name = 'Подрубрика'
        verbose_name_plural = 'Подрубрики'


class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Прошел активацию?')
    send_messages = models.BooleanField(default=True, verbose_name='Слать оповещения о новых комментариях?')

    class Meta(AbstractUser.Meta):
        pass
