from authentication.models import User
from common.models import ADDRESS_TYPE, BaseModel
from django.db import models


class Address(BaseModel):
    """
        Model for storing addresses.

        Attributes:
            user (ForeignKey): The user associated with the address.
            address (TextField): The address details.
            pin_code (CharField): The pin code of the address.
            city (CharField): The city of the address.
            state (CharField): The state of the address.
            country (CharField): The country of the address.
            type (CharField): The type of the address (e.g., default, billing, shipping).

        Meta:
            db_table (str): The name of the database table for the model.
            verbose_name (str): The human-readable name of the model in singular form.
            verbose_name_plural (str): The human-readable name of the model in plural form.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    address = models.TextField()
    pin_code = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    type = models.CharField(max_length=10, choices=ADDRESS_TYPE, default="default")

    class Meta:
        db_table = "addresses"
        verbose_name = "Address"
        verbose_name_plural = "Addresses"


class Vendor(BaseModel):
    """
        Model for storing vendor information.

        Attributes:
            user (OneToOneField): The user associated with the vendor.
            shop_name (CharField): The name of the vendor's shop.
            aadhar_number (CharField): The Aadhar number of the vendor.
            aadhar_image (JSONField): The JSON field to store Aadhar image details.
            pancard_number (CharField): The PAN card number of the vendor.
            pancard_image (JSONField): The JSON field to store PAN card image details.
            gst_number (CharField): The GST number of the vendor.
            business_license (JSONField): The JSON field to store business license details.
            is_verified (BooleanField): Indicates if the vendor is verified.
            is_document_added (BooleanField): Indicates if the vendor's documents are added.
            bio (TextField): The vendor's bio or profile summary.
            description (TextField): Additional description about the vendor.

        Meta:
            db_table (str): The name of the database table for the model.
            verbose_name (str): The human-readable name of the model in singular form.
            verbose_name_plural (str): The human-readable name of the model in plural form.

    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="vendor")
    shop_name = models.CharField(max_length=100)
    aadhar_number = models.CharField(max_length=12)
    aadhar_image = models.JSONField()
    pancard_number = models.CharField(max_length=10)
    pancard_image = models.JSONField()
    gst_number = models.CharField(max_length=15)
    business_license = models.JSONField()
    is_verified = models.BooleanField(default=False)
    is_document_added = models.BooleanField(default=False)
    bio = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "vendors"
        verbose_name = "Vendor"
        verbose_name_plural = "Vendors"
