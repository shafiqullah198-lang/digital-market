from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')

    def total_price(self):
        return sum(
            item.product.price * item.quantity
            for item in self.items.all()
        )

    def total_quantity(self):
        return sum(item.quantity for item in self.items.all())

    def __str__(self):
        return f"{self.user.username}'s cart"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
class Meta:
    unique_together = ('cart', 'product')
    def __str__(self):
        return f"{self.product.title} ({self.quantity})"

