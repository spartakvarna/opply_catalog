from django.db import models


class Product(models.Model):
    """Model of the Product entity."""

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()

    def __str__(self):
        return self.name
