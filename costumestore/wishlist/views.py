from common.permissions import IsCustomer
from rest_framework import permissions, viewsets
from rest_framework_simplejwt import authentication
from .serializers import WishlistSerializer
from .models import WishlistItem


# Create your views here.
class WishlistView(viewsets.ModelViewSet):
    """
    This view is used to perform CRUD operations on customer specific wishlist items.

    Args:
        viewsets (ModelViewSet): Handle CRUD operations

    Attributes:
        serializer_class: Serialize products information
        authentication_classes: Handle JWT authentication
        permission_classes: Only authenticate customer is allowed to access this view
    """

    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsCustomer]
    serializer_class = WishlistSerializer

    def get_queryset(self):
        return WishlistItem.objects.filter(wishlist__user=self.request.user)
