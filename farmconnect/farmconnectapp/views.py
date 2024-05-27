# farmconnectapp/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import FarmConnectApp
from products.serializers import ProductSerializer
from orders.serializers import OrderSerializer

class FilterProductsView(APIView):
    def get(self, request):
        category = request.query_params.get('category')
        price_range = request.query_params.getlist('price_range')
        location = request.query_params.get('location')

        if price_range:
            price_range = list(map(float, price_range))

        products = FarmConnectApp.filter_products(category=category, price_range=price_range, location=location)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProcessCheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        shipping_address = request.data.get('shipping_address')
        payment_info = request.data.get('payment_info')
        order = FarmConnectApp.process_checkout(request.user, shipping_address, payment_info)

        if order:
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)
