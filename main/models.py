from tabnanny import verbose
from django.db import models

# таблица для хранения данных excel
class table(models.Model):
    order = models.IntegerField("Заказ №")
    costDoll = models.IntegerField("Стоимость $")
    costRUB = models.FloatField("Стоимость ₽", default=0) 
    date = models.CharField('Срок поставки', max_length=30)

    def __str__(self):
        return self.order

    class Meta:
        verbose_name = 'Таблица'
        verbose_name_plural = 'Таблицы'

# таблица для тг бота
class orders(models.Model):
    ordernumber = models.IntegerField("Заказ №")