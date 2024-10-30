from django.db import models
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404, render
from .serializers import ProductSerializer
from .models import Product
from django.db.models import Q

# Product List View (GET and POST for Admin)
class ProductList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]  # Allow read-only for all, but restrict writes

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Only allow admin users to create new products
        if not request.user.is_staff:
            return Response({"detail": "Only admins can add products."}, status=status.HTTP_403_FORBIDDEN)
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Product Detail View (GET, PUT, DELETE)
class ProductDetail(APIView):
    def get(self, request, id):
        product = get_object_or_404(Product, id=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, id):
        # Restrict this view to admin users
        product = get_object_or_404(Product, id=id)
        if not request.user.is_staff:
            return Response({"detail": "Only admins can edit products."}, status=status.HTTP_403_FORBIDDEN)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        # Restrict this view to admin users
        product = get_object_or_404(Product, id=id)
        if not request.user.is_staff:
            return Response({"detail": "Only admins can delete products."}, status=status.HTTP_403_FORBIDDEN)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Product List Page View (for HTML rendering)
def product_list_page(request):
    query = request.GET.get('q')
    category = request.GET.get('category', '').strip().capitalize()
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()

    products = Product.objects.all()

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
    if category:
        products = products.filter(category__iexact=category)
    if min_price:
        try:
            min_price = float(min_price)
            products = products.filter(price__gte=min_price)
        except ValueError:
            pass
    if max_price:
        try:
            max_price = float(max_price)
            products = products.filter(price__lte=max_price)
        except ValueError:
            pass

    return render(request, 'products/product_list.html', {'products': products})

# Product Detail Page View (for HTML rendering)
def product_detail_page(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'products/product_detail.html', {'product': product})
