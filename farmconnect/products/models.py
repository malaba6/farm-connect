from django.db import models
from django.conf import settings
from shoppingcarts.models import ShoppingCart, CartItem

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    images = models.ImageField(upload_to='products/', null=True, blank=True)
    farmer = models.IntegerField()

    def __str__(self):
        return self.name

    def add_to_cart(self, user, quantity=1):
        cart, created = ShoppingCart.objects.get_or_create(user=user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=self)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()

    def edit_product(self, name=None, description=None, price=None, quantity=None, images=None):
        if name:
            self.name = name
        if description:
            self.description = description
        if price:
            self.price = price
        if quantity is not None:
            self.quantity = quantity
        if images:
            self.images = images
        self.save()

    def delete_product(self):
        self.delete()
