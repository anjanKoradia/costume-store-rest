from common.permissions import IsVendor
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Address, Vendor
from .serializers import AddressSerializer, VendorProfileSerializer


class UserAddress(APIView):
    """
        API view for user addresses.

        Authentication:
            - Requires JWT authentication.

        Permissions:
            - Requires the user to be authenticated.

        Methods:
            - GET: Retrieve all addresses associated with the authenticated user.
            - POST: Create a new address for the authenticated user.
            - PATCH: Update an existing address of the authenticated user.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
            Create a new address for the authenticated user.

            Args:
                request (Request): The HTTP request containing the address data.

            Returns:
                Response: The success message indicating if the address was stored successfully.

            Raises:
                Response with 400 status code if the request data is invalid.
        """
        try:
            address = Address.objects.filter(user=request.user)
            serializer = AddressSerializer(address, many=True)
        except Exception:
            return Response(
                {"message": "Address not found", "success": False},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
            Create a new address for the authenticated user.

            Args:
                request (Request): The HTTP request containing the address data.

            Returns:
                Response: The success message indicating if the address was stored successfully.

            Raises:
                Response with 400 status code if the request data is invalid.
        """
        serializer = AddressSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            created = serializer.save()
            if created:
                return Response(
                    {"message": "Address stored successfully", "success": True},
                    status=status.HTTP_201_CREATED,
                )
            return Response(
                {"message": "Address with same user is already exist", "success": True},
                status=status.HTTP_302_FOUND,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        """
            Update an existing address of the authenticated user.

            Args:
                request (Request): The HTTP request containing the updated address data.

            Returns:
                Response: The updated serialized address data.

            Raises:
                Response with 404 status code if the address is not found.
                Response with 400 status code if the request data is invalid.
        """
        try:
            address = Address.objects.get(
                user=request.user, type=request.data.get("type")
            )
        except Address.DoesNotExist:
            return Response(
                {"message": "Address not found", "success": False},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = AddressSerializer(address, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                {"message": "Address updated successfully", "success": True}
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorProfile(APIView):
    """
        API view for vendor profile.

        Authentication:
            - Requires JWT authentication.

        Permissions:
            - Requires the user to be authenticated.
            - Requires the user to have the role of "vendor".

        Methods:
            - GET: Retrieve the profile of the authenticated vendor.
            - POST: Create a new vendor profile for the authenticated user.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsVendor]

    def get(self, request):
        """
            Retrieve the profile of the authenticated vendor.

            Returns:
                Response: The serialized vendor profile data.

            Raises:
                Response with 404 status code if the vendor profile does not exist.
        """
        try:
            vendor = Vendor.objects.get(user=request.user)
            serializer = VendorProfileSerializer(vendor)
        except Vendor.DoesNotExist:
            return Response(
                {"message": "Vendor does not exist.", "success": False},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
            Create a new vendor profile for the authenticated user.

            Args:
                request (Request): The HTTP request containing the vendor profile data.

            Returns:
                Response: The success message indicating if the vendor profile was created successfully.

            Raises:
                Response with 400 status code if the request data is invalid.
        """
        serializer = VendorProfileSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            created = serializer.save()
            if created:
                return Response(
                    {"message": "Vendor profile created", "success": True},
                    status=status.HTTP_201_CREATED,
                )
            return Response(
                {"message": "Vendor profile already exist", "success": True},
                status=status.HTTP_302_FOUND,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
