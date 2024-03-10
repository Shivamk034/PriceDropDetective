from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Product(models.Model):
    
    url = models.CharField(blank=False,null=False,max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=300)
    image = models.CharField(max_length=300)

    class Meta:
        unique_together = [['user', 'url']]

class Price(models.Model):
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    price = models.CharField(max_length=300)

    timestamp = models.DateTimeField(blank=False,null=False,default=timezone.now)
