from django.contrib import admin

from .models import Color, Image, Size


@admin.register(Color)
class Colors(admin.ModelAdmin):
    """
        Admin configuration for the 'Color' model.

        Attributes:
            list_display (list): The fields to display in the admin list view.
    """
    list_display = ["name"]


@admin.register(Size)
class Sizes(admin.ModelAdmin):
    """
        Admin configuration for the 'Size' model.

        Attributes:
            list_display (list): The fields to display in the admin list view.
    """
    list_display = ["name"]


@admin.register(Image)
class Images(admin.ModelAdmin):
    """
        Admin configuration for the 'Image' model.

        Attributes:
            list_display (list): The fields to display in the admin list view.
    """
    list_display = ["url"]
