from common.models import USER_ROLE_CHOICES, BaseModel
from django.contrib.auth.models import AbstractUser
from django.db import models
from .manager import CustomUserManager


class User(AbstractUser, BaseModel):
    """
        Custom User model.

        Attributes:
            email (EmailField): The email address of the user (unique).
            name (CharField): The name of the user.
            phone (CharField): The phone number of the user.
            role (CharField): The role of the user (choices: USER_ROLE_CHOICES).
            profile_image (URLField, optional): The URL of the user's profile image. Defaults to blank.
            email_token (TextField, optional): The email verification token for the user. Defaults to blank.
            is_active (BooleanField): Indicates whether the user's account is active or not.
            objects (CustomUserManager): The custom user manager for this model.
    """
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    role = models.CharField(choices=USER_ROLE_CHOICES, max_length=10)
    profile_image = models.URLField(blank=True, null=True)
    email_token = models.TextField(blank=True)
    is_active = models.BooleanField(default=False)

    username = None
    first_name = None
    last_name = None

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"
