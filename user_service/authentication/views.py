from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Sign Up View
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.create_user(username=username, password=password)
        login(request, user)  # Log in the user after successful registration
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
@login_required
def home(request):
    return render(request, 'authentication/home.html')

# Logout View
@csrf_exempt
def logout_user(request):
    logout(request)
    return redirect('login')
