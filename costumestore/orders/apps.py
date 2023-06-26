from django.apps import AppConfig


class OrdersConfig(AppConfig):
    """
    Configuration for the 'common' app.

    Attributes:
        default_auto_field (str): The default auto field for model primary keys.
        name (str): The name of the app ('common').

    Methods:
        ready(): Performs actions when the app is ready to be used.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "orders"
