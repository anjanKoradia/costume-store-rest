from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from .models import User
from .serializers import RegisterUserSerializer


class RegisterUser(CreateAPIView):
    """
        View for registering a new user.

        Attributes:
            serializer_class (class): The serializer class to use for user registration.
            queryset (QuerySet): The queryset of User objects.
    """
    serializer_class = RegisterUserSerializer
    queryset = User.objects.all()

@api_view(["PATCH"])
def activate_user(request, email_token):
    """
        Activate a user account.

        Args:
            request (Request): The HTTP request object.
            email_token (str): The email token for identifying the user.

        Returns:
            Response: A response indicating the status of the account activation.
    """
    try:
        user = User.objects.get(email_token=email_token)
    except User.DoesNotExist:
        return Response({'message': 'User not found.', 'success': False}, status=status.HTTP_404_NOT_FOUND)

    if not user.is_active:
        user.is_active = True
        user.save()
        return Response({'message': 'Your account is activated.', 'success': True})

    return Response({'message': 'Your account is already active'})
