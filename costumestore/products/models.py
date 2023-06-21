from django.db import models
from accounts.models import Vendor
from common.models import BaseModel, Color, Image, Size, PRODUCT_CATEGORY
from django.core.validators import MinValueValidator, MaxValueValidator


class Product(BaseModel):
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


class ProductImages(Image):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_images"
    )

    class Meta:
        db_table = "product_images"
        verbose_name = "ProductImage"
        verbose_name_plural = "ProductImages"
