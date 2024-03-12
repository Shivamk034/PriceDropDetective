from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class Product(models.Model):
    
    url   = models.CharField(blank=False,null=False,max_length=300,unique=True)
    title = models.CharField(max_length=300)
    image = models.CharField(max_length=300)

    def __str__(self):
        return self.title

class Price(models.Model):
    
    product   = models.ForeignKey(Product, on_delete=models.CASCADE)
    price     = models.CharField(max_length=300)
    timestamp = models.DateTimeField(blank=False,null=False,default=timezone.now)

    def __str__(self):
        return f"{self.price}---------{self.product.title[:40]}"
class Track(models.Model):

    user    = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}---------{self.product.title[:40]}"