from django.db import models
from django.core.validators import MinValueValidator


class Order(models.Model):
    new = 'new'
    accepted = 'accepted'
    rejected = 'rejected'
    choices = [
        (accepted, 'accepted'),
        (rejected, 'rejected'),
    ]
    status = models.CharField(max_length=64, choices=choices, default=new)
    created_at = models.DateTimeField(auto_now_add=True)
    external_id = models.CharField(max_length=128)


class Product(models.Model):
    name = models.CharField('Product', max_length=64, unique=True)


class OrderDetail(models.Model):
    product = models.ForeignKey(Product, related_name='details', on_delete=models.PROTECT)
    amount = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=3)
    order = models.ForeignKey(Order, related_name='details', on_delete=models.CASCADE)