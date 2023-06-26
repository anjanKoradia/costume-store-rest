from rest_framework import generics, permissions, viewsets
from rest_framework_simplejwt import authentication
from common.permissions import IsCustomer, IsVendor
from .serializers import BillingDetailsSerializer, OrderItemsSerializer
from .models import BillingDetail, OrderItem


class CustomerOrderView(generics.ListCreateAPIView):
    """
    API view for managing customer orders.

    Attributes:
        - authentication_classes (list): The authentication classes applied to the view.
        - permission_classes (list): The permission classes applied to the view.
        - serializer_class (BillingDetailsSerializer): The serializer class for the view.

    Methods:
        - get_serializer_context: Get the context dictionary for the serializer.
        - get_queryset: Get the queryset of billing details for the current customer.

    """

    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsCustomer]
    serializer_class = BillingDetailsSerializer

    def get_serializer_context(self):
        """
        Get the context dictionary for the serializer.

        Returns:
            dict: The serializer context dictionary.

        """
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def get_queryset(self):
        """
        Get the queryset of billing details for the current customer.

        Returns:
            QuerySet: The queryset of billing details.

        """
        return BillingDetail.objects.filter(order__user=self.request.user)


class VendorOrderView(viewsets.ModelViewSet):
    """
    API view for managing vendor orders.

    Attributes:
        - authentication_classes (list): The authentication classes applied to the view.
        - permission_classes (list): The permission classes applied to the view.
        - serializer_class (OrderItemsSerializer): The serializer class for the view.

    Methods:
        - get_queryset: Get the queryset of order items for the current vendor.
        - get_serializer_context: Get the context dictionary for the serializer.

    """

    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsVendor]
    serializer_class = OrderItemsSerializer

    def get_queryset(self):
        """
        Get the queryset of order items for the current vendor.

        Returns:
            QuerySet: The queryset of order items.

        """
        return OrderItem.objects.filter(product__vendor__user=self.request.user)

    def get_serializer_context(self):
        """
        Get the context dictionary for the serializer.

        Returns:
            dict: The serializer context dictionary.

        """
        context = super().get_serializer_context()
        context["request"] = self.request
        return context
