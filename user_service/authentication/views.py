from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from verify_email.email_handler import send_verification_email
from django.core.exceptions import ValidationError
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserProfileForm
from django.db.models import ObjectDoesNotExist
from django.contrib import messages

# Register View with Email Verification
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Create the user instance but don't save it to the database yet
            user.is_active = False  # Set user as inactive until email verification
            user.save()  # Now save the user to the database

            try:
                # Send verification email
                send_verification_email(request, form)  # Pass form to send verification email correctly
                request.session['unverified_user_email'] = user.email  # Store the email in session
                return redirect('verification_sent')  # Redirect to verification message page
            except ValidationError as e:
                user.delete()  # If email sending fails, delete the user
                return render(request, 'authentication/register.html', {'form': form, 'error': str(e)})
    else:
        form = CustomUserCreationForm()

    return render(request, 'authentication/register.html', {'form': form})

def verification_sent(request):
    user_email = request.session.get('unverified_user_email', 'No email found')  # Retrieve email from session
    return render(request, 'authentication/verification_sent.html', {'user_email': user_email})


# Sign In View
@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Check if the user's email has been verified
            if user.is_active:
                login(request, user)  # Log in the user
                return redirect('home')
            else:
                return HttpResponse("Your account is inactive. Please verify your email.", status=400)
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

@login_required
def profile_view(request):
    # Create a profile for the user if it doesn't exist
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Error updating your profile.')
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'authentication/profile.html', {'form': form, 'user_profile': user_profile})
