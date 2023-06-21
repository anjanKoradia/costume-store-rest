from .models import Product
from rest_framework import status
from rest_framework import viewsets
from .serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


# Create your views here.
class VendorProduct(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        try:
            products = Product.objects.filter(vendor__user=request.user)
            serializer = ProductSerializer(data=products, many=True)

            if serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_302_FOUND)

            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                {"message": "Products not found", "success": False},
                status=status.HTTP_404_NOT_FOUND,
            )

    def create(self, request):
        serializer = ProductSerializer(data=request.data, context={"request": request})

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Product added successfully", "success": True},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            product = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            return Response(
                {"message": "Product not found", "success": False},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = ProductSerializer(
            product, data=request.data, partial=True, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Product details updated successfully", "success": True}
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            product = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            return Response(
                {"message": "Product not found", "success": False},
                status=status.HTTP_404_NOT_FOUND,
            )

        product.delete()
        return Response({"message": "Product deleted successfully", "success": True})
