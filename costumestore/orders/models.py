from django.core.validators import MinValueValidator
from accounts.models import Address
from products.models import Product
from django.db import models
from authentication.models import User
from common.models import BaseModel, ORDER_STATUS_TYPE


class Order(BaseModel):
    """
    Model representing an order placed by a user.

    Attributes:
    - user (ForeignKey): The user who placed the order.
    - amount (PositiveIntegerField): The total amount of the order.
    - order_note (TextField): Additional note or comment for the order.

    Meta:
    - db_table (str): The database table name for this model.
    - verbose_name (str): The human-readable name for a single object of this model.
    - verbose_name_plural (str): The human-readable name for multiple objects of this model.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    amount = models.PositiveIntegerField()
    order_note = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "orders"
        verbose_name = "Order"
        verbose_name_plural = "Orders"


class OrderItem(BaseModel):
    """
    Model representing an item within an order.

    Attributes:
    - order (ForeignKey): The order to which this item belongs.
    - product (ForeignKey): The product associated with the item.
    - status (CharField): The status of the order item.
    - quantity (PositiveIntegerField): The quantity of the item.
    - size (CharField): The size of the item.
    - color (CharField): The color of the item.

    Meta:
    - db_table (str): The database table name for this model.
    - verbose_name (str): The human-readable name for a single object of this model.
    - verbose_name_plural (str): The human-readable name for multiple objects of this model.
    """

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="items")
    status = models.CharField(
        max_length=10, default="placed", choices=ORDER_STATUS_TYPE
    )
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    size = models.CharField(max_length=5)
    color = models.CharField(max_length=20)

    class Meta:
        db_table = "order_items"
        verbose_name = "OrderItem"
        verbose_name_plural = "OrderItems"


class BillingDetail(BaseModel):
    """
    Model representing billing details associated with an order.

    Attributes:
    - order (OneToOneField): The order associated with the billing details.
    - name (CharField): The name for billing.
    - address (ForeignKey): The address for billing.
    - phone (CharField): The phone number for billing.
    - email (EmailField): The email address for billing.

    Meta:
    - db_table (str): The database table name for this model.
    - verbose_name (str): The human-readable name for a single object of this model.
    - verbose_name_plural (str): The human-readable name for multiple objects of this model.
    """

    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="billing_detail"
    )
    name = models.CharField(max_length=100)
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE, related_name="billing_detail"
    )
    phone = models.CharField(max_length=10)
    email = models.EmailField()

    class Meta:
        db_table = "billing_details"
        verbose_name = "BillingDetail"
        verbose_name_plural = "BillingDetails"
