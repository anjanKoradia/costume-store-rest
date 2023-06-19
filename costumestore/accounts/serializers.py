from .models import Vendor, Address
from rest_framework import serializers
from django.db.utils import DatabaseError
from cloudinary.exceptions import BadRequest
from common.services import CloudinaryServices
from rest_framework.exceptions import ValidationError


class VendorProfileSerializer(serializers.ModelSerializer):
    aadhar_image = serializers.ImageField(
        required=True, allow_empty_file=False, allow_null=False
    )
    pancard_image = serializers.ImageField(
        required=True, allow_empty_file=False, allow_null=False
    )
    business_license = serializers.ImageField(
        required=True, allow_empty_file=False, allow_null=False
    )

    class Meta:
        model = Vendor
        exclude = ["user"]

    def create(self, validated_data):
        data = validated_data

        try:
            aadhar_image_url = CloudinaryServices.store_image(
                data["aadhar_image"], data["shop_name"], "/documents"
            )
            pancard_image_url = CloudinaryServices.store_image(
                data["pancard_image"], data["shop_name"], "/documents"
            )
            business_license_url = CloudinaryServices.store_image(
                data["business_license"], data["shop_name"], "/documents"
            )
        except BadRequest as e:
            raise ValidationError("Something went wrong while uploading images.")

        try:
            vendor, created = Vendor.objects.get_or_create(
                user=self.context["request"].user,
                defaults={
                    "shop_name": data["shop_name"],
                    "aadhar_number": data["aadhar_number"],
                    "pancard_number": data["pancard_number"],
                    "gst_number": data["gst_number"],
                    "aadhar_image": aadhar_image_url,
                    "pancard_image": pancard_image_url,
                    "business_license": business_license_url,
                    "is_document_added": True,
                },
            )
        except DatabaseError as e:
            raise ValidationError(
                {
                    "message": "Somthing went wrong while creating vendor profile",
                    "success": False,
                }
            )

        return created


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ["user"]

    def create(self, validated_data):
        data = validated_data
        try:
            address, created = Address.objects.get_or_create(
                user=self.context["request"].user,
                type=data["type"],
                defaults={
                    "address": data["address"],
                    "pin_code": data["pin_code"],
                    "city": data["city"],
                    "state": data["state"],
                    "country": data["country"],
                },
            )
        except DatabaseError as e:
            raise ValidationError(
                {
                    "message": "Somthing went wrong while storing address",
                    "success": False,
                }
            )

        return created
