import uuid
from django.db import models
from authentication.models import User
from common.models import BaseModel, ADDRESS_TYPE


class Address(BaseModel):
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
