from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import ShoppingCart, CartItem
from products.models import Product
from .serializers import ShoppingCartsSerializer, CartItemSerializer

class ShoppingCartsView(APIView):
    permission_classes = [IsAuthenticated]

    def get_cart(self, user):
        cart, created = ShoppingCart.objects.get_or_create(user=user)
        return cart

    def get(self, request):
        cart = self.get_cart(request.user)
        serializer = ShoppingCartsSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        cart = self.get_cart(request.user)
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        cart.add_item(product, quantity)
        serializer = ShoppingCartsSerializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, product_id):
        cart = self.get_cart(request.user)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        cart.remove_item(product)
        serializer = ShoppingCartsSerializer(cart)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
