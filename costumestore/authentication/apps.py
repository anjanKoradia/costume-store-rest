from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    """
        Configuration for the 'products' app.

        Attributes:
            default_auto_field (str): The default auto field for model primary keys.
            name (str): The name of the app ('products').
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'
