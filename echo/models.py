from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from django.db import models


# Модель книги для базы данных
class Book(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    price = models.FloatField()

    class Meta:
        managed = False
        db_table = 'books'  # Привязка к таблице

    def __str__(self):
        return self.name


# Модель роли для базы данных
class Role(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'roles'

    def __str__(self):
        return self.name


# Модель юзера для базы данных
class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    login = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    role = models.ForeignKey('role', on_delete=models.PROTECT)      # Внешний ключ для ролей

    class Meta:
        managed = False
        db_table = 'users'

    def __str__(self):
        return self.name


# Модель заказа для базы данных
class Order(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(default=datetime.now()+timedelta(hours=5))  # По дефолту выставляет время заказа 
    price = models.FloatField()                                                     #(прибавляет 5 часов так как по дефолту ставит время UTC)
    user = models.ForeignKey('user', on_delete=models.PROTECT)

    class Meta:
        managed = False
        db_table = 'orders'

    def __str__(self):
        return self.name


# Модель книг в заказе для базы данных
class OrderBook(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey('order', on_delete=models.PROTECT)
    book = models.ForeignKey('book', on_delete=models.PROTECT)

    class Meta:
        managed = False
        db_table = 'orders_books'

    def __str__(self):
        return self.book.name