from .models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import RegisterUserSerializer
from rest_framework.generics import CreateAPIView

class RegisterUser(CreateAPIView):
    serializer_class = RegisterUserSerializer
    queryset = User.objects.all()

@api_view(["PATCH"])
def activate_user(request, email_token):
    try:
        user = User.objects.get(email_token=email_token)
    except User.DoesNotExist:
        return Response({'message': 'User not found.', 'success': False}, status=status.HTTP_404_NOT_FOUND)

    if not user.is_active:
        user.is_active = True
        user.save()
        return Response({'message': 'Your account is activated.', 'success': True})

    else:
        return Response({'message': 'Your account is already active'})