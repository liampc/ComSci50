from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    product = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=200, blank=True)
    lister = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.product} is ${self.price}"