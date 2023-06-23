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
    """
        Abstract base model class. To apply in all models.

        Attributes:
            id (UUIDField): Primary key field with a unique identifier.
            created_at (DateTimeField): Field representing the creation timestamp.
            updated_at (DateTimeField): Field representing the last update timestamp.

        Meta:
            abstract (bool): Specifies that this is an abstract base model.
    """
    id = models.UUIDField(
        primary_key=True, unique=True, default=uuid.uuid4, editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Color(BaseModel):
    """
        Model representing a color.

        Attributes:
            name (CharField): Field for the color name.

        Meta:
            db_table (str): The database table name for this model.
            verbose_name (str): The human-readable name for a single object of this model.
            verbose_name_plural (str): The human-readable name for multiple objects of this model.
    """
    name = models.CharField(max_length=20)

    class Meta:
        db_table = "colors"
        verbose_name = "Color"
        verbose_name_plural = "Colors"


class Size(BaseModel):
    """
        Model representing a size.

        Attributes:
            name (CharField): Field for the size name.

        Meta:
            db_table (str): The database table name for this model.
            verbose_name (str): The human-readable name for a single object of this model.
            verbose_name_plural (str): The human-readable name for multiple objects of this model.
    """
    name = models.CharField(max_length=20, choices=SIZE_CHOICES)

    class Meta:
        db_table = "sizes"
        verbose_name = "Size"
        verbose_name_plural = "Sizes"


class Image(BaseModel):
    """
        Model representing an image.

        Attributes:
            url (URLField): Field for the image URL.
            public_id (CharField): Field for the public identifier of the image.
            location (CharField): Field for the location of the image.

        Meta:
            db_table (str): The database table name for this model.
            verbose_name (str): The human-readable name for a single object of this model.
            verbose_name_plural (str): The human-readable name for multiple objects of this model.
    """
    url = models.URLField()
    public_id = models.CharField(max_length=100)
    location = models.CharField(max_length=20, default="Cloudinary")

    class Meta:
        db_table = "images"
        verbose_name = "Image"
        verbose_name_plural = "Images"
