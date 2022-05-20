# Generated by Django 4.0.4 on 2022-05-20 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='table',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='№')),
                ('order', models.IntegerField(verbose_name='Заказ №')),
                ('costDoll', models.IntegerField(verbose_name='Стоимость $')),
                ('costRUB', models.IntegerField(verbose_name='Стоимость ₽')),
                ('date', models.DateField(verbose_name='Срок поставки')),
            ],
        ),
    ]