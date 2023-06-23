from django.contrib import admin
from .models import User


@admin.register(User)
class BaseUser(admin.ModelAdmin):
    """
        Model admin for managing User objects in the admin panel.

        Attributes:
            list_display (list): The fields to display in the User list view.
    """
    list_display = ["id", "email", "name", "phone", "role"]
