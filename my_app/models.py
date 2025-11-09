from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models
class Category(models.Model):
    name=models.CharField(max_length=25)
class Product(models.Model):
    name=models.CharField(max_length=25)
    barcode=models.BigIntegerField()
    sell_price=models.FloatField()
    unit_in_stock=models.IntegerField()
    photo=models.ImageField(upload_to="media/",null=True,blank=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
class User(AbstractUser):
    pass