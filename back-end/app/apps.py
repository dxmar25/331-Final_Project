from django.apps import AppConfig


class AppConfig(AppConfig):
    """
    This is a AppConfig class derived from Django's AppConfig class

    It configures the Django backend
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
