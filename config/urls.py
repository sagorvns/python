"""
URL configuration for task_backend project.

This file tells Django which views to serve for which URLs.
Think of it as the "table of contents" for your web application.
When a user visits a URL, Django looks here to know which function/view to call.
"""
from django.contrib import admin
from django.urls import path, include

# URL patterns - these map URLs to views
urlpatterns = [
    # Admin panel URL - Django's built-in admin interface
    # Visit http://localhost:8000/admin to access the admin panel
    path('admin/', admin.site.urls),
    
    # API URLs - all our Task API endpoints will be under /api/
    # When someone visits /api/, Django will look in the 'api' app's urls.py
    path('api/', include('api.urls')),
]


