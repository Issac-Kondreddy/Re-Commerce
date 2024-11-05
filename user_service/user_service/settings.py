from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-j%vc)n=o1ktuqjv!o(gg7+($tgh12=!v0sodl3%j^sxca^l6wg"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # Set to False in production

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
 # Add your domain or IP address here in production


# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "authentication",  # Your custom authentication app
    "rest_framework",
    "rest_framework.authtoken",  # DRF Token authentication
    'django.contrib.sites',  # Required by Django Allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',  # Enable social logins if required
    'allauth.socialaccount.providers.google',  # Google OAuth provider
    "verify_email.apps.VerifyEmailConfig",  # Email verification app
    'phonenumber_field'
]


# OAuth2 settings for Google
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'OAUTH_PKCE_ENABLED': False,
    }
}


# Automatically log the user in after Google login/signup
SOCIALACCOUNT_AUTO_SIGNUP = True
ACCOUNT_EMAIL_VERIFICATION = 'none'  # Skip email verification for social login
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_LOGIN_ON_GET = True  # Automatically log in after returning from Google


# Redirect URLs after login and signup
LOGIN_REDIRECT_URL = '/authentication/home/' # Redirect to home after login
ACCOUNT_LOGOUT_REDIRECT_URL = '/authentication/login/'  # Redirect to login page after logout
LOGIN_URL = '/authentication/login/'  # Redirect to login page if not authenticated

# Django Rest Framework Settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',  # Add this line
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = "user_service.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'Templates'],  # Set your custom templates directory
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "user_service.wsgi.application"


# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",  # Static files directory
]
STATIC_ROOT = BASE_DIR / "staticfiles"  # Collect static files in production

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Security settings for CSRF and session management
CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SAMESITE = 'Strict'
CSRF_COOKIE_HTTPONLY = False  # False since we might grab it via universal-cookies
SESSION_COOKIE_HTTPONLY = True

# Use the following settings in production:
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True

# Email configuration for sending email verifications
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'issackondreddy@gmail.com'  # Replace with your email
EMAIL_HOST_PASSWORD = 'qhvm yuqz dune qywj'  # Replace with your app password

DEFAULT_FROM_EMAIL = 'issackondreddy@gmail.com'  

# Sites Framework
SITE_ID = 2  # Required for Django Allauth

# Email verification custom settings (Optional)
HTML_MESSAGE_TEMPLATE = "authentication/email_message.html"
VERIFICATION_SUCCESS_TEMPLATE = "authentication/success.html"
VERIFICATION_FAILED_TEMPLATE = "authentication/failed.html"

# Expire email verification link after 1 day
EXPIRE_AFTER = "1d"

# Allow the user to resend the email 3 times before limiting
MAX_RETRIES = 3

# Authentication backends for both regular and social login
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

