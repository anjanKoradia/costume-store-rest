from django.db import models
from common.models import BaseModel
from authentication.models import User
from products.models import Product


class Wishlist(BaseModel):
    """
    Model representing a user's wishlist.

    Fields:
        user (User): The user associated with the wishlist.
        total_price (int): The total price of all items in the wishlist.

    Meta:
        db_table (str): The database table name for the model.
        verbose_name (str): The human-readable name for a single object of the model.
        verbose_name_plural (str): The human-readable name for multiple objects of the model.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wishlist")
    total_price = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "wishlists"
        verbose_name = "Wishlist"
        verbose_name_plural = "Wishlists"


class WishlistItem(BaseModel):
    """
    Model representing an item in the wishlist.

    Fields:
        wishlist (Wishlist): The wishlist associated with the item.
        product (Product): The product associated with the item.

    Meta:
        db_table (str): The database table name for the model.
        verbose_name (str): The human-readable name for a single object of the model.
        verbose_name_plural (str): The human-readable name for multiple objects of the model.
    """

    wishlist = models.ForeignKey(
        Wishlist, on_delete=models.CASCADE, related_name="items"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="wishlist_items"
    )

    class Meta:
        db_table = "wishlist_items"
        verbose_name = "WishlistItem"
        verbose_name_plural = "WishlistItems"
