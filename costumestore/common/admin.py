from django.contrib import admin
from .models import Color, Size, Image


@admin.register(Color)
class Color(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Size)
class Size(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Image)
class Image(admin.ModelAdmin):
    list_display = ["url"]
