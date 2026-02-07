"""
Django settings for task_backend project.

This file contains all the configuration for your Django application.
Think of it as the "control center" where you can adjust database settings,
installed apps, middleware, security settings, and more.
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR is the root directory of your project
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
# This key is used for cryptographic signing. Never share this in production!
SECRET_KEY = 'django-insecure-change-this-in-production-for-security'

# SECURITY WARNING: don't run with debug turned on in production!
# Debug mode shows detailed error pages. Set to False in production.
DEBUG = True

# ALLOWED_HOSTS: List of host/domain names that this Django site can serve.
# Empty means localhost. Add your domain here when deploying.
ALLOWED_HOSTS = []


# Application definition
# INSTALLED_APPS: List of all Django applications that are enabled in this project.
# Each app provides features like models, views, admin interface, etc.
INSTALLED_APPS = [
    'django.contrib.admin',          # Django's built-in admin interface
    'django.contrib.auth',           # Authentication system
    'django.contrib.contenttypes',   # Content types framework
    'django.contrib.sessions',       # Session framework
    'django.contrib.messages',       # Messaging framework
    'django.contrib.staticfiles',    # Static files handling (CSS, JS, images)
    
    # Third-party apps
    'rest_framework',                # Django REST Framework - for building APIs
    'corsheaders',                   # CORS (Cross-Origin Resource Sharing) - allows React to communicate with Django
    
    # Local apps (our apps)
    'api',                           # Our API app where we'll define our Task model and endpoints
]

# MIDDLEWARE: Components that process requests/responses globally.
# They execute in the order listed below.
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # CORS middleware - MUST be at the top to allow cross-origin requests
    'django.middleware.security.SecurityMiddleware',  # Security enhancements
    'django.contrib.sessions.middleware.SessionMiddleware',  # Manages sessions
    'django.middleware.common.CommonMiddleware',  # Common utilities
    'django.middleware.csrf.CsrfViewMiddleware',  # CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # User authentication
    'django.contrib.messages.middleware.MessageMiddleware',  # Messages handling
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Clickjacking protection
]

# ROOT_URLCONF: Points to the main URL configuration file
ROOT_URLCONF = 'config.urls'

# TEMPLATES: Configuration for Django's template system
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI_APPLICATION: Points to the WSGI application for deployment
WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
# We're using SQLite3, which is a file-based database perfect for development.
# No installation needed - it's built into Python!
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # SQLite database engine
        'NAME': BASE_DIR / 'db.sqlite3',         # Database file location
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS Configuration
# CORS (Cross-Origin Resource Sharing) allows your React frontend (running on different port)
# to make requests to your Django backend. Without this, browsers block cross-origin requests.
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Vite's default port for React development server
    "http://127.0.0.1:5173",  # Alternative localhost format
]

# Alternatively, you can allow all origins during development (NOT for production!)
# CORS_ALLOW_ALL_ORIGINS = True  # Uncomment this if you have CORS issues, but remember to remove in production!

# REST Framework Configuration
# Django REST Framework settings for API behavior
REST_FRAMEWORK = {
    # Default pagination - useful when you have many tasks
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,  # Number of items per page
    
    # Default permission classes - who can access the API
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # Allow anyone to access (change in production!)
    ],
}


