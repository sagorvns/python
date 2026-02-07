"""
Serializers for the API app.

Serializers in Django REST Framework convert complex data types (like Django models)
into Python native data types that can be easily converted to JSON for API responses.
They also handle converting JSON data back into Python objects when creating/updating.

Think of serializers as translators between:
- Python/Django objects (Task model) ↔ JSON (what React receives)
"""
from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model.
    
    ModelSerializer automatically generates fields based on the model.
    It handles validation, creation, and updating of Task instances.
    
    Why use a serializer?
    1. Converts Task objects to JSON for API responses
    2. Validates incoming JSON data before saving to database
    3. Handles the creation and updating of Task instances
    """
    
    class Meta:
        """
        Meta class defines which model and fields the serializer should work with.
        
        model: The Django model this serializer is based on
        fields: Which fields from the model to include in the API
        '__all__' means include all fields from the Task model
        """
        model = Task
        fields = '__all__'  # Include all fields: title, description, completed, created_at, updated_at
    
    def validate_title(self, value):
        """
        Custom validation for the title field.
        
        This method is automatically called by the serializer to validate the title.
        It ensures the title is not empty or just whitespace.
        
        Args:
            value: The title value being validated
            
        Returns:
            The validated title (after stripping whitespace)
            
        Raises:
            ValidationError: If the title is empty after stripping
        """
        # Strip leading and trailing whitespace
        value = value.strip()
        
        # Check if title is empty after stripping
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        
        return value


