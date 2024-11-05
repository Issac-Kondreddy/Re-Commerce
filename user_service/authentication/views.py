# authentication/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from verify_email.email_handler import send_verification_email
from django.core.exceptions import ValidationError
from .forms import CustomUserCreationForm, UserProfileForm
from .models import UserProfile
from django.contrib import messages

# Register View with Email Verification
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Set inactive until email verification
            user.save()

            try:
                send_verification_email(request, form)
                request.session['unverified_user_email'] = user.email
                return redirect('verification_sent')
            except ValidationError as e:
                user.delete()
                return render(request, 'authentication/register.html', {'form': form, 'error': str(e)})
    else:
        form = CustomUserCreationForm()
    return render(request, 'authentication/register.html', {'form': form})

# Verification sent confirmation
def verification_sent(request):
    user_email = request.session.get('unverified_user_email', 'No email found')
    return render(request, 'authentication/verification_sent.html', {'user_email': user_email})

# Sign In View
@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('home')
            else:
                return HttpResponse("Your account is inactive. Please verify your email.", status=400)
        return HttpResponse("Invalid Credentials", status=400)
    return render(request, 'authentication/login.html')

# Home View (Requires Login)
@never_cache
@login_required
def home(request):
    return render(request, 'authentication/home.html')

# Logout View
@csrf_exempt
def logout_user(request):
    logout(request)
    return redirect('login')

# Profile View (Requires Login)
@login_required
def profile_view(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'authentication/profile.html', {'form': form, 'user_profile': user_profile})
