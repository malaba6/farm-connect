# shoppingCarts/urls.py
from django.urls import path
from .views import ShoppingCartsView

urlpatterns = [
    path('shopping-cart/', ShoppingCartsView.as_view(), name='shopping-cart-view'),
    path('shopping-cart/item/<int:product_id>/', ShoppingCartsView.as_view(), name='shopping-cart-item-manage'),
]
