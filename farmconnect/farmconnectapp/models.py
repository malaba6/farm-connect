from django.db import models
from products.models import Product
from orders.models import Order
from django.db.models import Q

class FarmConnectApp:
    @staticmethod
    def filter_products(category=None, price_range=None, location=None):
        products = Product.objects.all()
        if category:
            products = products.filter(category=category)
        if price_range:
            products = products.filter(price__gte=price_range[0], price__lte=price_range[1])
        if location:
            products = products.filter(farmer__location=location)
        return products

    @staticmethod
    def process_checkout(user, shipping_address, payment_info):
        cart = user.shopping_cart
        if not cart.items.exists():
            return None

        order = Order.objects.create(
            user=user,
            shipping_address=shipping_address,
            payment_info=payment_info,
            total_price=cart.total_price,
        )
        for cart_item in cart.items.all():
            order.products.add(cart_item.product, through_defaults={'quantity': cart_item.quantity})
        cart.items.all().delete()  # Clear the cart after checkout
        cart.total_price = 0
        cart.save()
        return order
