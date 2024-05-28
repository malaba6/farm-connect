from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Product
from .serializers import ProductSerializer
from django.db import IntegrityError
from django.http import Http404

class ProductListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: ProductSerializer(many=True)},
        security=[{'Bearer': []}]
    )
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, default="Sample Product"),
                'description': openapi.Schema(type=openapi.TYPE_STRING, default="This is a sample product description."),
                'price': openapi.Schema(type=openapi.TYPE_NUMBER, format='float', default=99.99),
                'quantity': openapi.Schema(type=openapi.TYPE_INTEGER, default=10),
            },
            required=['name', 'description', 'price', 'quantity']
        ),
        responses={
            201: ProductSerializer,
            400: "Bad Request"
        },
        security=[{'Bearer': []}]
    )
    def post(self, request):
        serializer = ProductSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            product = serializer.save()
            return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        responses={200: ProductSerializer, 404: "Not Found"},
        security=[{'Bearer': []}]
    )
    def get(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, default="Updated Product"),
                'description': openapi.Schema(type=openapi.TYPE_STRING, default="This is an updated product description."),
                'price': openapi.Schema(type=openapi.TYPE_NUMBER, format='float', default=89.99),
                'quantity': openapi.Schema(type=openapi.TYPE_INTEGER, default=20),
            },
        ),
        responses={
            200: ProductSerializer,
            400: "Bad Request",
            403: "Forbidden",
            404: "Not Found"
        },
        security=[{'Bearer': []}]
    )
    def put(self, request, pk):
        product = self.get_object(pk)
        if product.farmer != request.user.id:
            return Response({"error": "You are not authorized to edit this product."}, status=status.HTTP_403_FORBIDDEN)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={
            204: "No Content",
            403: "Forbidden",
            404: "Not Found"
        },
        security=[{'Bearer': []}]
    )
    def delete(self, request, pk):
        product = self.get_object(pk)
        if product.farmer != request.user.id:
            return Response({"error": "You are not authorized to delete this product."}, status=status.HTTP_403_FORBIDDEN)
        product.delete_product()
        return Response(status=status.HTTP_204_NO_CONTENT)
