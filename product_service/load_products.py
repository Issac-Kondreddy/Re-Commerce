import csv
import os
import django
from products.models import Product  # Replace 'myproductapp' with your app name

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "product_service.settings") 
django.setup()

def load_products_from_csv(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Product.objects.create(
                name=row['name'],
                description=row['description'],
                price=float(row['price']),
                stock=int(row['stock'])
            )
    print("Products loaded successfully!")

# Run the function with the path to products.csv
load_products_from_csv('products.csv')
