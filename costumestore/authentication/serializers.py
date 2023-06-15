from .models import User
from rest_framework import serializers
from common.validators import is_valid_password

class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'role']

    def to_representation(self, instance):
        response = {
            "message": "Your account has been created successfully !!",
            "success": True
        }
        return response

    def validate_password(self, value):
        is_valid_password(value)
        return value