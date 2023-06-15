import uuid
from rest_framework import status
from django.dispatch import receiver
from authentication.models import User
from rest_framework.response import Response
from django.db.models.signals import post_save
from .services import send_account_activation_email


# signal to create vendor profile and to send account activation email
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        try:
            user = User.objects.get(email=instance.email)
        except User.DoesNotExist:
            return Response({'message': 'User not found.', 'success': False}, status=status.HTTP_404_NOT_FOUND)

        email_token = str(uuid.uuid4())
        user.email_token = email_token
        user.save()

        # send_account_activation_email(instance.name,instance.email,email_token)
