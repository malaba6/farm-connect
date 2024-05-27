from django.db import models
from django.conf import settings
from products.models import Product

class ShoppingCarts(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='shopping_cart')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"ShoppingCart of {self.user.username}"

    def add_item(self, product, quantity=1):
        cart_item, created = CartItem.objects.get_or_create(shopping_cart=self, product=product)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()
        self.calculate_total()

    def remove_item(self, product):
        try:
            cart_item = CartItem.objects.get(shopping_cart=self, product=product)
            cart_item.delete()
            self.calculate_total()
        except CartItem.DoesNotExist:
            pass

    def calculate_total(self):
        self.total_price = sum(item.product.price * item.quantity for item in self.items.all())
        self.save()

class CartItem(models.Model):
    shopping_cart = models.ForeignKey(ShoppingCarts, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"
