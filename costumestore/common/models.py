import uuid
from django.db import models

USER_ROLE_CHOICES = (("customer", "Customer"), ("vendor", "Vendor"), ("admin", "Admin"))

ADDRESS_TYPE = (
    ("billing", "Billing"),
    ("default", "Default"),
)

PRODUCT_CATEGORY = (
    ("mens", "Men's"),
    ("women", "Women's"),
    ("kids", "Kid's"),
    ("cosmetics", "Cosmetics"),
    ("accessories", "Accessories"),
)

SIZE_CHOICES = (
    ("XS", "Extra Small"),
    ("S", "Small"),
    ("M", "Medium"),
    ("L", "Large"),
    ("XL", "Extra Large"),
    ("XXL", "Extra Extra Large"),
)


class BaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True, unique=True, default=uuid.uuid4, editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Color(BaseModel):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = "colors"
        verbose_name = "Color"
        verbose_name_plural = "Colors"


class Size(BaseModel):
    name = models.CharField(max_length=20, choices=SIZE_CHOICES)

    class Meta:
        db_table = "sizes"
        verbose_name = "Size"
        verbose_name_plural = "Sizes"


class Image(BaseModel):
    url = models.URLField()
    public_id = models.CharField(max_length=100)
    location = models.CharField(max_length=20, default="Cloudinary")

    class Meta:
        db_table = "images"
        verbose_name = "Image"
        verbose_name_plural = "Images"
