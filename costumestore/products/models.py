from accounts.models import Vendor
from common.models import PRODUCT_CATEGORY, BaseModel, Color, Image, Size
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Product(BaseModel):
    """
        A model representing a product.

        Args:
            BaseModel (type): The base model class.

        Attributes:
            vendor (ForeignKey): The vendor associated with the product.
            name (CharField): The name of the product.
            colors (ManyToManyField): The available colors for the product.
            sizes (ManyToManyField): The available sizes for the product.
            category (CharField): The category of the product.
            subcategory (CharField, optional): The subcategory of the product.
            rating (PositiveIntegerField): The rating of the product.
            price (PositiveIntegerField): The price of the product.
            discount (PositiveIntegerField): The discount percentage for the product.
            stock (PositiveIntegerField): The available stock of the product.
            description (TextField): The description of the product.

        Meta:
            db_table (str): The name of the database table for the model.
            verbose_name (str): The singular name for the model.
            verbose_name_plural (str): The plural name for the model.
    """
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, related_name="products"
    )
    name = models.CharField(max_length=200)
    colors = models.ManyToManyField(Color)
    sizes = models.ManyToManyField(Size)
    category = models.CharField(max_length=20, choices=PRODUCT_CATEGORY)
    subcategory = models.CharField(
        max_length=50, blank=True, null=True, default="Clothing"
    )
    rating = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    stock = models.PositiveIntegerField(default=1)
    description = models.TextField()

    class Meta:
        db_table = "products"
        verbose_name = "Product"
        verbose_name_plural = "Products"


class ProductImage(Image):
    """_summary_
        A model representing images associated with a product.

        Args:
            Image (type): The base model class for images.

        Attributes:
            product (ForeignKey): The product associated with the image.

        Meta:
            db_table (str): The name of the database table for the model.
            verbose_name (str): The singular name for the model.
            verbose_name_plural (str): The plural name for the model.
    """
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_images"
    )

    class Meta:
        db_table = "product_images"
        verbose_name = "ProductImage"
        verbose_name_plural = "ProductImages"
