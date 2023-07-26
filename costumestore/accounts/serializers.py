from rest_framework import serializers, response
from common.services import CloudinaryServices
from .models import Address, Vendor


class VendorProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for vendor profile creation.

    Attributes:
        aadhar_image (ImageField): The Aadhar image of the vendor.
        pancard_image (ImageField): The PAN card image of the vendor.
        business_license (ImageField): The business license image of the vendor.

    Meta:
        model (Vendor): The model associated with the serializer.
        exclude (list): The list of fields to exclude from serialization.
    """

    aadhar_image = serializers.ImageField(
        required=True, allow_empty_file=False, allow_null=False,
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
        """
        Create a vendor profile.

        Args:
            validated_data (dict): The validated data for creating the vendor profile.

        Returns:
            bool: The success status indicating if the vendor profile was created.

        Raises:
            ValidationError: If there is an error while uploading the images or creating the vendor profile.
        """
        data = validated_data
        try:
            aadhar_image_url = CloudinaryServices.store_image(
                self, image=data["aadhar_image"], folder=data["shop_name"]
            )
            pancard_image_url = CloudinaryServices.store_image(
                self, image=data["pancard_image"], folder=data["shop_name"]
            )
            business_license_url = CloudinaryServices.store_image(
                self, image=data["business_license"], folder=data["shop_name"]
            )
        except Exception:
            return response.Response(
                {
                    "message": "Something went wrong while uploading images.",
                    "success": False,
                }
            )

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
        except Exception:
            return response.Response(
                {
                    "message": "Somthing went wrong while creating vendor profile",
                    "success": False,
                }
            )
        return created


class AddressSerializer(serializers.ModelSerializer):
    """
    Serializer for address creation.

    Meta:
        model (Address): The model associated with the serializer.
        exclude (list): The list of fields to exclude from serialization.
    """

    class Meta:
        model = Address
        exclude = ["user"]

    def create(self, validated_data):
        """
        Create an address.

        Args:
            validated_data (dict): The validated data for creating the address.

        Returns:
            bool: The success status indicating if the address was created.

        Raises:
            ValidationError: If there is an error while creating the address.
        """
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
        except Exception:
            return response.Response(
                {
                    "message": "Something went wrong while storing address",
                    "success": False,
                }
            )

        return address
