from django.db import models
from django.contrib.auth.models import AbstractUser
from .utilities import get_timestamp_path

"""
    Модель рубрики объявления. 
    Порядок имеет индекс, поэтому запросы к БД
    будут выполняться быстро    
"""
class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True, verbose_name='Порядок')
    order = models.SmallIntegerField(default=0, db_index=True, verbose_name='Порядок')
    super_rubric = models.ForeignKey('SuperRubric', on_delete=models.PROTECT, null=True,
                                     blank=True, verbose_name='Надрубрика')

    """
    Менеджер для надрубрик. 
    Возвращает только надрубрики
    """
class SuperRubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=True)

    """
    Надрубрика.
    Proxy модель для Rubric.
    """
class SuperRubric(Rubric):
    object = SuperRubricManager()

    def __str__(self):
        return self.name

    class Meta:
        proxy = True
        ordering = ['order', 'name']
        verbose_name = 'Надрубрика'
        verbose_name_plural = 'Надрубрики'

    """
    Менеджер для подрубрик. 
    Возвращает только подрубрики
    """
class SubRubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=False)

    """
    Подрубрика.
    Proxy модель для Rubric.
    """
class SubRubric(Rubric):
    object = SubRubricManager()

    def __str__(self):
        return '%s - %s' % (self.super_rubric.name, self.name)

    class Meta:
        proxy = True
        ordering = ['super_rubric__order', 'super_rubric__name', 'order', 'name']
        verbose_name = 'Подрубрика'
        verbose_name_plural = 'Подрубрики'

    """
    Модель пользователя.
    """
class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Прошел активацию?')
    send_messages = models.BooleanField(default=True, verbose_name='Слать оповещения о новых комментариях?')

    def delete(self, *args, **kwargs):
        for bb in self.bb_set.all():
            bb.delete()
        super().delete(*args, **kwargs)

    class Meta(AbstractUser.Meta):
        pass

    """
    Модель объявления.
    """
class Bb(models.Model):
    rubric = models.ForeignKey (SubRubric, on_delete=models.PROTECT, verbose_name='Рубрика')
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

    """
    Модель дополнительного изображения.
    """
class AdditionalImage(models.Model):
    bb = models.ForeignKey(Bb, on_delete=models.CASCADE, verbose_name='Объявление')
    image = models.ImageField(upload_to=get_timestamp_path, verbose_name='Изображение')

    class Meta:
        verbose_name_plural = 'Дополнительные иллюстрации'
        verbose_name = 'Дополнительная иллюстрация'



