# orders/views.py

from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Cart, CartItem, Order, OrderItem
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()

@method_decorator(csrf_exempt, name='dispatch')
class AddToCartView(View):
    def post(self, request):
        # Temporary mock user for testing
        user, _ = User.objects.get_or_create(username="testuser")
        cart, _ = Cart.objects.get_or_create(user=user)

        # Ensure a default price for the mock product
        product_id = int(request.POST.get("product_id", 1))
        product_name = "Sample Product"
        product_price = float(request.POST.get("product_price", 10.00))  # Default price set to 10.00 if not provided
        quantity = int(request.POST.get("quantity", 1))

        # Check if item is already in the cart
        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart,
            product_id=product_id,
            defaults={"product_name": product_name, "product_price": product_price, "quantity": quantity}
        )

        if not item_created:
            cart_item.quantity += quantity
            cart_item.save()

        return JsonResponse({"success": True, "message": "Item added to cart", "quantity": cart_item.quantity})

@method_decorator(csrf_exempt, name='dispatch')  # Temporary CSRF exemption for testing
class ViewCartView(View):
    def get(self, request):
        # Temporary mock user for testing
        user, _ = User.objects.get_or_create(username="testuser")

        # Retrieve the user's cart
        try:
            cart = Cart.objects.get(user=user)
            cart_items = cart.items.all()  # Get all items related to this cart

            # Prepare cart data
            cart_data = {
                "user": user.username,
                "items": [
                    {
                        "product_id": item.product_id,
                        "product_name": item.product_name,
                        "product_price": float(item.product_price),
                        "quantity": item.quantity,
                        "total_price": float(item.product_price * item.quantity),
                    }
                    for item in cart_items
                ],
                "total_cart_value": float(sum(item.product_price * item.quantity for item in cart_items)),
            }

            return JsonResponse({"success": True, "cart": cart_data})

        except Cart.DoesNotExist:
            return JsonResponse({"success": False, "message": "Cart is empty."})


@method_decorator(csrf_exempt, name='dispatch')
class RemoveFromCartView(View):
    def post(self, request):
        # Temporary mock user for testing
        user = request.user if request.user.is_authenticated else User.objects.get(username="testuser")
        cart = Cart.objects.get(user=user)
        product_id = request.POST.get("product_id")

        # Remove the cart item if it exists
        try:
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
            cart_item.delete()
            return JsonResponse({"success": True, "message": "Item removed from cart."})
        except CartItem.DoesNotExist:
            return JsonResponse({"success": False, "message": "Item not found in cart."})


@method_decorator(csrf_exempt, name='dispatch')
class PlaceOrderView(View):
    def post(self, request):
        # Temporary mock user
        user, _ = User.objects.get_or_create(username="testuser")

        # Retrieve cart and items
        cart = Cart.objects.get(user=user)
        cart_items = cart.items.all()

        # Calculate total order price
        total_price = sum(item.product_price * item.quantity for item in cart_items)

        # Create the order
        order = Order.objects.create(user=user, total_price=total_price)

        # Add items to the order
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product_name=item.product_name,
                product_price=item.product_price,
                quantity=item.quantity
            )
            item.delete()  # Remove item from cartt

        # Send confirmation email
        send_mail(
            subject="Order Confirmation",
            message=f"Thank you for your order, {user.username}! Your order ID is {order.id} with total amount ${total_price}.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=["vissujnv@gmail.com"]
        )

        return JsonResponse({"success": True, "message": "Order placed successfully!", "order_id": order.id})

@method_decorator(csrf_exempt, name='dispatch')
class OrderHistoryView(View):
    def get(self, request):
        # Temporary mock user for testing
        user = request.user if request.user.is_authenticated else User.objects.get(username="testuser")

        # Retrieve all orders for the user
        orders = Order.objects.filter(user=user).order_by('-created_at')
        
        # Structure the order data with items and total price
        order_history = [
            {
                "order_id": order.id,
                "created_at": order.created_at,
                "total_price": float(order.total_price),
                "items": [
                    {
                        "product_name": item.product_name,
                        "product_price": float(item.product_price),
                        "quantity": item.quantity,
                        "total_price": float(item.product_price * item.quantity)
                    } for item in order.items.all()
                ]
            }
            for order in orders
        ]

        return JsonResponse({"success": True, "orders": order_history})