from django.contrib import admin
from .models import Product, ProductImages


@admin.register(Product)
class Product(admin.ModelAdmin):
    list_display = ["name", "price", "category", "stock"]


@admin.register(ProductImages)
class ProductImages(admin.ModelAdmin):
    list_display = ["product", "url", "public_id"]
