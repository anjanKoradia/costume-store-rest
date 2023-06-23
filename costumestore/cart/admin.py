from django.contrib import admin
from .models import Cart, CartItem

@admin.register(Cart)
class Carts(admin.ModelAdmin):
    """
        Admin model for managing carts.

        Attributes:
            list_display (list): The list of fields to display in the admin list view.
    """
    list_display = ["user", "total_price"]


@admin.register(CartItem)
class CartItems(admin.ModelAdmin):
    """
    Admin model for managing cart items.

    Attributes:
        list_display (list): The list of fields to display in the admin list view.

    """
    list_display = ["cart", "product", "quantity", "size", "color"]
