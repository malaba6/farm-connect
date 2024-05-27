from django.urls import path
from .views import FilterProductsView, ProcessCheckoutView

urlpatterns = [
    path('filter-products/', FilterProductsView.as_view(), name='filter-products'),
    path('process-checkout/', ProcessCheckoutView.as_view(), name='process-checkout'),
]
