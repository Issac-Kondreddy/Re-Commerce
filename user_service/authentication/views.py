from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.views.decorators.cache import never_cache

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if the email is already registered
        if User.objects.filter(email=email).exists():
            return render(request, 'authentication/register.html', {
                'error': 'Email is already in use.'
            })

        # Create the user with additional fields
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
        login(request, user)
        return redirect('login')

    return render(request, 'authentication/register.html')


# Sign In View
@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Log in the user
            return redirect('home')
        else:
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
