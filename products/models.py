from django.db import models


class Product(models.Model):
    """Model of the Product entity.

    Products should be soft delete always.
    """

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class Customer(models.Model):
    """Model of the Customer entity."""

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Order(models.Model):
    """Model of the Order entity."""

    datetime = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Products should be soft-deleted always
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Products should be soft-deleted always
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()

    def __str__(self):
        return f"Order {self.id} by {self.customer}"
