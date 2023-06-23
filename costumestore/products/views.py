from common.permissions import IsVendor
from rest_framework import permissions, viewsets
from rest_framework_simplejwt import authentication
from .models import Product
from .serializers import ProductSerializer


class ProductView(viewsets.ReadOnlyModelViewSet):
    """
        This view is used to display all products, and it's information

        Args:
            viewsets (ReadOnlyModelViewSet): Allow only read operations

        Attributes:
            queryset (QuerySet): Return all products
            serializer_class: Serialize products information
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class VendorProduct(viewsets.ModelViewSet):
    """
        This view is used to perform CRUD operations on vendor specific products and it's information

        Args:
            viewsets (ModelViewSet): Handle CRUD operations

        Attributes:
            serializer_class: Serialize products information
            authentication_classes: Handle JWT authentication
            permission_classes: Only authenticate vendor is allowed to access this view
    """
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsVendor]
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(vendor__user=self.request.user)
