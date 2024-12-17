from django.apps import AppConfig

class ResponsesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'responses'

    def ready(self):
        """Initialize Firebase when the app is ready"""
        from .services.firebase_service import initialize_firebase
        initialize_firebase()