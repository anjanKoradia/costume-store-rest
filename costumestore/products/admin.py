from django.contrib import admin

from .models import Product, ProductImages


@admin.register(Product)
class Product(admin.ModelAdmin):
    """
       Admin configuration for the 'Product' model.

       Attributes:
           list_display (list): The fields to display in the admin list view.
    """
    list_display = ["name", "price", "category", "stock"]


@admin.register(ProductImages)
class ProductImages(admin.ModelAdmin):
    """
       Admin configuration for the 'ProductImages' model.

       Attributes:
           list_display (list): The fields to display in the admin list view.
    """
    list_display = ["product", "url", "public_id"]
