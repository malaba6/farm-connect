# shoppingCarts/tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from products.models import Product
from .models import ShoppingCarts, CartItem

User = get_user_model()

class ShoppingCartsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.product = Product.objects.create(
            name='Tomatoes', description='Fresh tomatoes', price=2.50, quantity=100, images=None, farmer=self.user
        )

    def test_add_item_to_cart(self):
        response = self.client.post('/api/shopping-cart/', {'product_id': self.product.id, 'quantity': 2})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['items'][0]['product']['name'], 'Tomatoes')
        self.assertEqual(response.data['items'][0]['quantity'], 2)

    def test_view_cart(self):
        self.client.post('/api/shopping-cart/', {'product_id': self.product.id, 'quantity': 2})
        response = self.client.get('/api/shopping-cart/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['items'][0]['product']['name'], 'Tomatoes')

    def test_remove_item_from_cart(self):
        self.client.post('/api/shopping-cart/', {'product_id': self.product.id, 'quantity': 2})
        response = self.client.delete(f'/api/shopping-cart/item/{self.product.id}/')
        self.assertEqual(response.status_code, 204)
        response = self.client.get('/api/shopping-cart/')
        self.assertEqual(response.data['items'], [])

    def test_update_item_quantity_in_cart(self):
        self.client.post('/api/shopping-cart/', {'product_id': self.product.id, 'quantity': 2})
        response = self.client.put(f'/api/shopping-cart/item/{self.product.id}/', {'quantity': 5})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['items'][0]['quantity'], 5)
