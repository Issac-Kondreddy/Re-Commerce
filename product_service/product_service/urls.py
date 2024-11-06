from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("products.urls")),  # API path with no duplication
    path("", RedirectView.as_view(url="/products/page/", permanent=False)),  # Redirect root to product page
    path("", include("products.urls")),  # Include products.urls directly, no "products/" prefix
]
