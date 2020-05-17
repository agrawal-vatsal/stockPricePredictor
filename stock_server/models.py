from django.db import models


# Create your models here.

class Stock(models.Model):
    name = models.CharField(max_length=20, null=False)
    date = models.CharField(max_length=20, null=False)
    price = models.FloatField(null=False)
    polarity_positive = models.BooleanField(default=False)
