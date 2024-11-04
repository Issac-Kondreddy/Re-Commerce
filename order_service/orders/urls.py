# orders/urls.py

from django.urls import path
from .views import AddToCartView,ViewCartView,RemoveFromCartView,PlaceOrderView,OrderHistoryView

urlpatterns = [
    path('add-to-cart/', AddToCartView.as_view(), name='add_to_cart'),
    path('view-cart/', ViewCartView.as_view(), name='view_cart'),
    path('remove-from-cart/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('place-order/', PlaceOrderView.as_view(), name='place_order'),
    path('order-history/', OrderHistoryView.as_view(), name='order_history'),
]
