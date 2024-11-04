# orders/views.py

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View
from .models import Cart, CartItem, Product
from django.conf import settings

class AddToCartView(View):
    def post(self, request):
        user = request.user  # Assuming user is authenticated
        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("quantity", 1))

        # Get or create the user's cart
        cart, created = Cart.objects.get_or_create(user=user)

        # Get the product or return a 404 if not found
        product = get_object_or_404(Product, id=product_id)

        # Check if item is already in the cart
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={"quantity": quantity, "price": product.price})

        if not item_created:
            # Update the quantity if item already exists in cart
            cart_item.quantity += quantity
            cart_item.save()

        return JsonResponse({"success": True, "message": "Item added to cart", "quantity": cart_item.quantity})
