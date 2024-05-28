from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'quantity', 'images']

    def create(self, validated_data):
        farmer = self.context['request'].user
        product = Product.objects.create(farmer=farmer.id, **validated_data)
        return product