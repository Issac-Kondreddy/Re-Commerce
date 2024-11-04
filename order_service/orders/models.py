from django.db import models
from django.conf import settings  # To access the User model

# Define Product model first
class Product(models.Model):
    id = models.IntegerField(primary_key=True)  # Primary key to match the product ID in Product Service
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False  # Prevent Django from creating a new table
        db_table = 'product_service_product'  # Reference if accessible; else leave it as a local placeholder

    def __str__(self):
        return self.name

# Define Cart model
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

# Define CartItem model
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product_id = models.IntegerField()  # Store product ID directly
    product_name = models.CharField(max_length=255)  # Store product name directly
    product_price = models.DecimalField(max_digits=10, decimal_places=2)  # Store product price directly
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product_name} in {self.cart}"


# orders/models.py

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.product_name}"
