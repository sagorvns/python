from django.apps import AppConfig


class ApiConfig(AppConfig):
    """
    Configuration class for the API app.
    
    This class tells Django about our API application.
    It allows Django to discover and load the app's models, views, etc.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'


