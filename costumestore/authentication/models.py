from django.db import models
from .manager import CustomUserManager
from django.contrib.auth.models import AbstractUser
from common.models import BaseModel, USER_ROLE_CHOICES


class User(AbstractUser, BaseModel):
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
