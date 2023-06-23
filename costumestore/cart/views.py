from common.permissions import IsCustomer
from rest_framework import permissions, viewsets
from rest_framework_simplejwt import authentication
from .serializers import CartSerializer
from .models import CartItem


# Create your views here.
class CartView(viewsets.ModelViewSet):
    """
        This view is used to perform CRUD operations on customer specific cart items.

        Args:
            viewsets (ModelViewSet): Handle CRUD operations

        Attributes:
            serializer_class: Serialize products information
            authentication_classes: Handle JWT authentication
            permission_classes: Only authenticate customer is allowed to access this view
    """
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsCustomer]
    serializer_class = CartSerializer

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)
