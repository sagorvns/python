"""
Views for the API app.

Views in Django REST Framework handle HTTP requests and return HTTP responses.
ViewSets combine the logic for multiple related views (list, create, retrieve, update, delete)
into a single class, which makes our code cleaner and more organized.

Why use ViewSets?
- Automatically provides CRUD operations (Create, Read, Update, Delete)
- Less code to write compared to writing separate views for each operation
- Automatically generates API endpoints based on the ViewSet
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Task model that provides CRUD operations.
    
    ModelViewSet automatically provides:
    - list: GET /api/tasks/ (get all tasks)
    - create: POST /api/tasks/ (create a new task)
    - retrieve: GET /api/tasks/{id}/ (get a specific task)
    - update: PUT /api/tasks/{id}/ (update a task - all fields required)
    - partial_update: PATCH /api/tasks/{id}/ (update a task - only provided fields)
    - destroy: DELETE /api/tasks/{id}/ (delete a task)
    
    Attributes:
        queryset: All Task objects that this ViewSet can work with
        serializer_class: The serializer to use for converting Task objects to/from JSON
    """
    
    # queryset: Defines which database records this ViewSet will work with
    # Task.objects.all() means all tasks in the database
    queryset = Task.objects.all()
    
    # serializer_class: Tells the ViewSet which serializer to use
    # This serializer handles converting Task objects to JSON and vice versa
    serializer_class = TaskSerializer
    
    @action(detail=True, methods=['patch'])
    def toggle_complete(self, request, pk=None):
        """
        Custom action to toggle the completed status of a task.
        
        This creates a custom endpoint: PATCH /api/tasks/{id}/toggle_complete/
        
        The @action decorator adds custom endpoints to the ViewSet.
        detail=True means this action works on a single task (not the list).
        methods=['patch'] means this endpoint only accepts PATCH requests.
        
        Args:
            request: The HTTP request object
            pk: The primary key (id) of the task to toggle
            
        Returns:
            Response with the updated task data or error message
        """
        # Get the specific task by its primary key (id)
        task = self.get_object()
        
        # Toggle the completed status (if True, becomes False; if False, becomes True)
        task.completed = not task.completed
        
        # Save the changes to the database
        task.save()
        
        # Serialize the updated task to JSON
        serializer = self.get_serializer(task)
        
        # Return the updated task data as JSON response
        return Response(serializer.data)


