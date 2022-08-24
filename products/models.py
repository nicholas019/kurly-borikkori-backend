from django.db import models


class Product(models.Model):
    name  = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    image = models.CharField(max_length=150)

    class Meta:
        db_table = 'products'

