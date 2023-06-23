from django.db import models
from django.core.validators import MinValueValidator
from common.models import SIZE_CHOICES, BaseModel
from authentication.models import User
from products.models import Product


class Cart(BaseModel):
    """
        Model representing a user's shopping cart.

        Fields:
            user (User): The user associated with the cart.
            total_price (int): The total price of all items in the cart.

        Meta:
            db_table (str): The database table name for the model.
            verbose_name (str): The human-readable name for a single object of the model.
            verbose_name_plural (str): The human-readable name for multiple objects of the model.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    total_price = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "carts"
        verbose_name = "Cart"
        verbose_name_plural = "Carts"


class CartItem(BaseModel):
    """
        Model representing an item in the shopping cart.

        Fields:
            cart (Cart): The cart associated with the item.
            product (Product): The product associated with the item.
            quantity (int): The quantity of the product in the cart.
            size (str): The size of the product.
            color (str): The color of the product.

        Meta:
            db_table (str): The database table name for the model.
            verbose_name (str): The human-readable name for a single object of the model.
            verbose_name_plural (str): The human-readable name for multiple objects of the model.
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="cart_items"
    )
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    size = models.CharField(max_length=3, choices=SIZE_CHOICES)
    color = models.CharField(max_length=20)

    class Meta:
        db_table = "cart_items"
        verbose_name = "CartItem"
        verbose_name_plural = "CartItems"
