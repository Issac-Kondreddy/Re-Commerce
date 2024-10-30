from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Product

class ProductAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a sample product
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=99.99,
            stock=10
        )
        self.product_list_url = reverse('product-list')
        self.product_detail_url = reverse('product-detail', kwargs={'id': self.product.id})

    def test_get_all_products(self):
        response = self.client.get(self.product_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_product_detail(self):
        response = self.client.get(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_product(self):
        # You will need an admin user to create a product
        self.client.force_authenticate(user=self._create_admin_user())
        data = {
            "name": "New Test Product",
            "description": "New Test Description",
            "price": 149.99,
            "stock": 5
        }
        response = self.client.post(self.product_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_product(self):
        # Update requires admin
        self.client.force_authenticate(user=self._create_admin_user())
        data = {
            "name": "Updated Test Product",
            "description": "Updated Description",
            "price": 199.99,
            "stock": 3
        }
        response = self.client.put(self.product_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_product(self):
        # Delete requires admin
        self.client.force_authenticate(user=self._create_admin_user())
        response = self.client.delete(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def _create_admin_user(self):
        from django.contrib.auth.models import User
        return User.objects.create_superuser('admin', 'admin@test.com', 'password123')
