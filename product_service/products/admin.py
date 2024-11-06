from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock')  # Display category, price, and stock in list view
    search_fields = ('name', 'description')  # Enable search by name and description
    list_filter = ('category', 'price')  # Add filters for category and price
    ordering = ('name',)  # Default ordering by name
    list_editable = ('category', 'price', 'stock')  # Make category, price, and stock editable in list view
    list_per_page = 20  # Display 20 items per page

    # Optional: Organize fields in the detail view
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'price', 'stock', 'category')
        }),
    )
