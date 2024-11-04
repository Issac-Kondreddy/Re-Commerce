from django.db import models
from django.conf import settings  # To access the User model

# Assuming the Product model is available from the Product Service
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    # Placeholder for Product ForeignKey; we will define the relationship in the next step
    product = models.ForeignKey('product_service.Product', on_delete=models.CASCADE)  
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.cart}"
