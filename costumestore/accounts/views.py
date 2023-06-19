from rest_framework import status
from .models import Vendor, Address
from common.permissions import IsVendor
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import VendorProfileSerializer, AddressSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication


class UserAddress(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            address = Address.objects.filter(user=request.user)
            serializer = AddressSerializer(address, many=True)
        except Exception as e:
            return Response(
                {"message": "Address not found", "success": False},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
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
                {"message": "Address updated successfully", "success": True},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorProfile(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsVendor]

    def get(self, request):
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
