from django.contrib import admin
from .models import Wishlist, WishlistItem


@admin.register(Wishlist)
class Wishlists(admin.ModelAdmin):
    """
    Admin model for managing wishlist.

    Attributes:
        list_display (list): The list of fields to display in the admin list view.
    """

    list_display = ["user", "total_price"]


@admin.register(WishlistItem)
class WishlistItems(admin.ModelAdmin):
    """
    Admin model for managing wishlist items.

    Attributes:
        list_display (list): The list of fields to display in the admin list view.
    """

    list_display = ["wishlist", "product"]
