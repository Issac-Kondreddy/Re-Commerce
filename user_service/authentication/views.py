# authentication/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from .forms import CustomUserCreationForm, UserProfileForm
from .models import UserProfile
from .utils import email_verification_token
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string

# Register view with email verification
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Set user as inactive until email verification
            user.save()

            # Generate token and build verification URL
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            verification_url = request.build_absolute_uri(
                reverse('verify_email', kwargs={'uidb64': uid, 'token': token})
            )

            # Render HTML message for the email
            email_subject = 'Verify your email address'
            email_message = render_to_string('authentication/email_verification.html', {
                'user': user,
                'verification_url': verification_url
            })

            # Send the verification email
            send_mail(
                email_subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
                html_message=email_message  # Include HTML message
            )

            request.session['unverified_user_email'] = user.email
            messages.success(request, "Registration successful! Please check your email to verify your account.")
            return redirect('verification_sent')
    else:
        form = CustomUserCreationForm()

    return render(request, 'authentication/register.html', {'form': form})


# Verification Sent Confirmation View
def verification_sent(request):
    user_email = request.session.get('unverified_user_email', 'No email found')
    return render(request, 'authentication/verification_sent.html', {'user_email': user_email})

# Verify Email View
def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_object_or_404(User, pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and email_verification_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your email has been verified. You can now log in.')
        return redirect('login')
    else:
        messages.error(request, 'Verification link is invalid or has expired.')
        return redirect('register')

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
                return redirect(settings.LOGIN_REDIRECT_URL)  # Use LOGIN_REDIRECT_URL from settings
            else:
                return HttpResponse("Your account is inactive. Please verify your email.", status=400)
        return HttpResponse("Invalid Credentials", status=400)
    return render(request, 'authentication/login.html')

# Home View (Requires Login)
@never_cache
@login_required
def dashboard(request):
    return render(request, 'authentication/dashboard.html')

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
