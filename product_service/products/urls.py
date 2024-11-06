from django.urls import path
from .views import ProductList, ProductDetail, product_list_page, product_detail_page

urlpatterns = [
    path('products/', ProductList.as_view(), name='product-list'),
    path('products/<int:id>/', ProductDetail.as_view(), name='product-detail'),
    path('products/page/', product_list_page, name='product-list-page'),
    path('products/page/<int:id>/', product_detail_page, name='product-detail-page'),
]
