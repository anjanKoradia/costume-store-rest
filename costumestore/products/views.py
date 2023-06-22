from .models import Product
from rest_framework import status
from rest_framework import viewsets
from common.permissions import IsVendor
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import ProductSerializer, GetProductSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication


class ProductView(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = GetProductSerializer


class VendorProduct(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsVendor]

    def get_queryset(self):
        return Product.objects.filter(vendor__user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "POST" or self.request.method == "PUT":
            return ProductSerializer
        return GetProductSerializer
