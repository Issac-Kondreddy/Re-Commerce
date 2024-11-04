# orders/urls.py

from django.urls import path
from .views import AddToCartView

urlpatterns = [
    path('add-to-cart/', AddToCartView.as_view(), name='add_to_cart'),
]
