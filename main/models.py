from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import re

# Create your models here.


class Product(models.Model):
    
    url   = models.CharField(blank=False,null=False,max_length=600,unique=True)
    title = models.CharField(max_length=600)
    image = models.CharField(max_length=600)

    def __str__(self):
        return self.title

class Price(models.Model):
    
    product   = models.ForeignKey(Product, on_delete=models.CASCADE)
    price     = models.CharField(max_length=50)
    timestamp = models.DateTimeField(blank=False,null=False,default=timezone.now)

    def __str__(self):
        return f"{self.price}---------{self.product.title[:40]}"
    
    @staticmethod
    def convertPrice(price):  
        return float(re.sub(r'[^0-9.]', '',price))
    @classmethod
    def isValidPrice(cls,price):
        try:
            cls.convertPrice(price)
            return True
        except:
            return False

    def floatPrice(self):  
        return self.convertPrice(self.price)


class Track(models.Model):

    user    = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}---------{self.product.title[:40]}"