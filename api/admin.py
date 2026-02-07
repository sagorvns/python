"""
Admin configuration for the API app.

The Django admin interface is a built-in tool that lets you manage your database
records through a web interface. This file registers models so they appear in the admin.
"""
from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the Task model.
    
    This class customizes how Tasks appear in Django's admin panel.
    list_display: Fields to show in the admin list view
    list_filter: Fields you can filter by in the admin
    search_fields: Fields you can search in the admin
    """
    # Fields to display in the task list in admin panel
    list_display = ('title', 'completed', 'created_at', 'updated_at')
    
    # Fields that can be used to filter tasks in the admin panel
    list_filter = ('completed', 'created_at')
    
    # Fields that can be searched in the admin panel
    search_fields = ('title', 'description')


