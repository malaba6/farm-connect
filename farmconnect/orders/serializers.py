from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer
from products.models import Product

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    products = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True, write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'order_items', 'products', 'status', 'total_price', 'shipping_address', 'payment_info']

    def create(self, validated_data):
        products = validated_data.pop('products')
        order = Order.objects.create(**validated_data)
        for product in products:
            OrderItem.objects.create(order=order, product=product, quantity=product.quantity)
        return order
