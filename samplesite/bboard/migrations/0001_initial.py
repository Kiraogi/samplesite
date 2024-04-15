# Generated by Django 5.0.4 on 2024-04-14 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bb',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Название товара')),
                ('content', models.TextField(verbose_name='Описание товара')),
                ('price', models.FloatField(verbose_name='Цена товара')),
                ('published', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')),
            ],
        ),
    ]
