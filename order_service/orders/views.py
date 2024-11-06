from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from .models import Cart, CartItem, Order, OrderItem
from django.contrib.auth import get_user_model
import json
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect

User = get_user_model()

# Add to Cart View
@method_decorator(csrf_exempt, name='dispatch')
class AddToCartView(View):
    def post(self, request):
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body.decode('utf-8'))
            product_id = data.get("product_id")
            product_price = data.get("product_price")
            quantity = data.get("quantity", 1)
            
            # Validate required fields
            if product_id is None or product_price is None:
                return JsonResponse({"success": False, "message": "Product ID and price are required."}, status=400)

            # Convert values to the required types
            product_id = int(product_id)
            product_price = float(product_price)
            quantity = int(quantity)

            # Use a mock user for testing
            user, _ = User.objects.get_or_create(username="testuser")
            cart, _ = Cart.objects.get_or_create(user=user)

            # Check if item is already in the cart
            cart_item, item_created = CartItem.objects.get_or_create(
                cart=cart,
                product_id=product_id,
                defaults={"product_name": "Sample Product", "product_price": product_price, "quantity": quantity}
            )

            # Update quantity if item already exists
            if not item_created:
                cart_item.quantity += quantity
                cart_item.save()

            return JsonResponse({"success": True, "message": "Item added to cart", "quantity": cart_item.quantity})
        
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid JSON format."}, status=400)
        except (ValueError, TypeError) as e:
            return JsonResponse({"success": False, "message": str(e)}, status=400)



# View Cart
@method_decorator(csrf_exempt, name='dispatch')
class ViewCartView(View):
    def get(self, request):
        user, _ = User.objects.get_or_create(username="testuser")

        try:
            cart = Cart.objects.get(user=user)
            cart_items = cart.items.all()

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

            return render(request, 'orders/cart.html', {'cart': cart_data})

        except Cart.DoesNotExist:
            return render(request, 'orders/cart.html', {'cart': None, 'message': 'Cart is empty.'})


@method_decorator(csrf_exempt, name='dispatch')
class RemoveFromCartView(View):
    def post(self, request):
        # Get the user and cart
        user = request.user if request.user.is_authenticated else User.objects.get(username="testuser")
        cart = Cart.objects.get(user=user)
        product_id = request.POST.get("product_id")

        # Try to find and delete the item in the cart
        try:
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
            cart_item.delete()
        except CartItem.DoesNotExist:
            pass  # If the item doesn't exist, do nothing

        # Redirect back to the cart page after item removal
        return HttpResponseRedirect(reverse('view_cart'))


# Place Order
@method_decorator(csrf_exempt, name='dispatch')
class PlaceOrderView(View):
    def post(self, request):
        user, _ = User.objects.get_or_create(username="testuser")
        cart = Cart.objects.get(user=user)
        cart_items = cart.items.all()
        total_price = sum(item.product_price * item.quantity for item in cart_items)

        order = Order.objects.create(user=user, total_price=total_price)
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product_name=item.product_name,
                product_price=item.product_price,
                quantity=item.quantity
            )
            item.delete()

        send_mail(
            subject="Order Confirmation",
            message=f"Thank you for your order, {user.username}! Your order ID is {order.id} with a total amount of ${total_price}.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=["vissujnv@gmail.com"]
        )

        # Redirect to the order confirmation page
        return redirect('order_confirmation', order_id=order.id)

# Order Confirmation
@method_decorator(csrf_exempt, name='dispatch')
class OrderConfirmationView(View):
    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            order_data = {
                'order_id': order.id,
                'total_amount': order.total_price,
                'order_date': order.created_at,
            }
        except Order.DoesNotExist:
            order_data = {
                'order_id': order_id,
                'total_amount': 99.99,
                'order_date': '2024-11-04'
            }

        return render(request, 'orders/order_confirmation.html', order_data)


# Order History
@method_decorator(csrf_exempt, name='dispatch')
class OrderHistoryView(View):
    def get(self, request):
        user = request.user if request.user.is_authenticated else User.objects.get(username="testuser")
        orders = Order.objects.filter(user=user).order_by('-created_at')
        
        order_history = [
            {
                "order_id": order.id,
                "created_at": order.created_at,
                "total_price": order.total_price
            }
            for order in orders
        ]

        return render(request, 'orders/order_history.html', {'orders': order_history})


# Order Detail
@method_decorator(csrf_exempt, name='dispatch')
class OrderDetailView(View):
    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            order_data = {
                "order_id": order.id,
                "created_at": order.created_at,
                "total_price": order.total_price,
                "items": [
                    {
                        "product_name": item.product_name,
                        "product_price": item.product_price,
                        "quantity": item.quantity,
                        "total_price": item.product_price * item.quantity
                    }
                    for item in order.items.all()
                ]
            }
            return render(request, 'orders/order_detail.html', {'order': order_data})
        except Order.DoesNotExist:
            return JsonResponse({"success": False, "message": "Order not found."}, status=404)
