"""
Models for the API app.

A Model in Django is a Python class that represents a database table.
When you define a model, Django automatically creates the database table for you.
Think of models as blueprints for your data structure.
"""
from django.db import models


class Task(models.Model):
    """
    Task model representing a task in the task manager.
    
    This model defines the structure of the Task table in the database.
    Each field in the model becomes a column in the database table.
    
    Fields:
        title: The name/title of the task (required, max 200 characters)
        description: Detailed description of what the task involves (optional, can be blank)
        completed: Whether the task has been completed (defaults to False)
        created_at: Timestamp when the task was created (automatically set)
    """
    
    # CharField is used for short text fields (like titles, names, etc.)
    # max_length specifies the maximum number of characters allowed
    # This is required because CharField must have a maximum length
    title = models.CharField(max_length=200)
    
    # TextField is used for longer text content (like descriptions, articles, etc.)
    # blank=True means the field is optional (can be empty in forms)
    # null=True means the field can be NULL in the database
    # We use both for maximum flexibility
    description = models.TextField(blank=True, null=True)
    
    # BooleanField stores True/False values
    # default=False means new tasks start as incomplete
    completed = models.BooleanField(default=False)
    
    # DateTimeField stores date and time information
    # auto_now_add=True means this field is automatically set to the current date/time
    # when the task is first created (and never changes)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # DateTimeField with auto_now=True updates every time the task is saved
    # This is useful for tracking when a task was last modified
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        """
        String representation of the Task model.
        
        This method defines how a Task object is displayed when converted to a string.
        For example, when you see a task in Django admin, this is what shows up.
        """
        return self.title
    
    class Meta:
        """
        Meta class for additional model configuration.
        
        ordering: Specifies the default order when querying tasks
        -created_at means descending order (newest first)
        Use ['created_at'] for ascending order (oldest first)
        """
        ordering = ['-created_at']  # Newest tasks appear first


