from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth import authenticate, login, logout
from .serializers import UserRegistrationSerializer, UserLoginSerializer
from django.contrib.auth.models import User

class UserRegistrationView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, default="testuser12"),
                'email': openapi.Schema(type=openapi.TYPE_STRING, default="testuser12@example.com"),
                'password': openapi.Schema(type=openapi.TYPE_STRING, default="testpassword"),
                'password2': openapi.Schema(type=openapi.TYPE_STRING, default="testpassword"),
                'is_farmer': openapi.Schema(type=openapi.TYPE_BOOLEAN, default=True),
                'is_consumer': openapi.Schema(type=openapi.TYPE_BOOLEAN, default=False),
            },
            required=['username', 'email', 'password', 'password2']
        ),
        responses={
            201: openapi.Response(
                description="User registered successfully",
                examples={
                    "application/json": {
                        "message": "User registered successfully!",
                        "data": {
                            "id": 1,
                            "username": "testuser12",
                            "email": "swaggeruser@example.com",
                            "is_farmer": True,
                            "is_consumer": False
                        }
                    }
                }
            ),
            400: "Bad Request"
        }
    )
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user_data = UserRegistrationSerializer(user).data 
            
            return Response(
                {
                    "message": "User registered successfully!",
                    "data": user_data
                 }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, default="testuser12"),
                'password': openapi.Schema(type=openapi.TYPE_STRING, default="testpassword"),
            },
            required=['username', 'password']
        ),

        responses={
            200: openapi.Response(
                description="Login successful",
                examples={
                    "application/json": {
                        "refresh": "your-refresh-token",
                        "access": "your-access-token"
                    }
                }
            ),
            401: "Unauthorized"
        }
    )
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class UserLogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
