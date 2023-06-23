from common.validators import is_valid_password
from rest_framework import serializers
from .models import User


class RegisterUserSerializer(serializers.ModelSerializer):
    """
        Serializer for registering a new user.

        Attributes:
            name (str): The name of the user.
            email (str): The email address of the user.
            password (str): The password of the user.
            role (str): The role of the user.
    """
    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'role']

    def to_representation(self, instance):
        """
            Custom representation for the serialized instance.

            Args:
                instance: The instance being serialized.

            Returns:
                dict: A custom response with a success message.
        """
        response = {
            "message": "Your account has been created successfully !!",
            "success": True
        }
        return response

    def validate_password(self, value):
        """
            Validate the password field.

            Args:
                value (str): The password value to validate.

            Returns:
                str: The validated password value.

            Raises:
                serializers.ValidationError: If the password is invalid.
        """
        is_valid_password(value)
        return value
