# authentication/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('home/', views.home, name='home'),
    path('profile/', views.profile_view, name='profile'),
    path('verification_sent/', TemplateView.as_view(template_name="authentication/verification_sent.html"), name='verification_sent'),
    
    # Email Verification
    path('verify-email/<uidb64>/<token>/', views.verify_email, name='verify_email'),

    # Password Reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='authentication/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='authentication/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='authentication/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='authentication/password_reset_complete.html'), name='password_reset_complete'),
]
