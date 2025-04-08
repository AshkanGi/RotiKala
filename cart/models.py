from django.db import models
from account.models import User
from product.models import Product


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total_price = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
    size = models.CharField(max_length=15)
    color = models.CharField(max_length=15)
    quantity = models.PositiveSmallIntegerField(default=0)
    price = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.product.name


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='address')
    full_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=11)
    province = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    address = models.TextField(max_length=150)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.user.username} -- {self.province}'


class DiscountCode(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name='Code Name')
    discount = models.PositiveIntegerField(default=0, verbose_name='Discount (%)')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Quantity Available')

    def __str__(self):
        return f"Code: {self.name} | Discount: {self.discount}% | Quantity: {self.quantity}"