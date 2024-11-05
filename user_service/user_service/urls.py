# user_service/urls.py

from django.contrib import admin
from django.urls import path, include
from . import views  # Assuming you have a `project_home` view in views.py
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("authentication/", include("authentication.urls")),
    path("accounts/", include("allauth.urls")),
    path("", views.project_home, name="project_home"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
