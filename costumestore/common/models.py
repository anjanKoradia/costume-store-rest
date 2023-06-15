import uuid
from django.db import models

USER_ROLE_CHOICES = (
    ("customer", "customer"),
    ("vendor", "vendor"),
    ("admin", "admin")
)

# Create your models here.
class BaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True, unique=True, default=uuid.uuid4, editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
