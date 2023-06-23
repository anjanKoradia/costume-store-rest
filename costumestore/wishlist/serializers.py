from rest_framework import serializers, response
from .models import WishlistItem


class WishlistSerializer(serializers.ModelSerializer):
    """
    Serializer for the WishlistItem model.

    Attributes:
        - All fields of the WishlistItem model.

    Methods:
        - create: Create a new cart item or update an existing one.
        - update: Update the quantity of a cart item based on the specified operation.
    """

    class Meta:
        model = WishlistItem
        fields = "__all__"

    def create(self, validated_data):
        """
        Create a new wishlist item

        Args:
            validated_data (dict): The validated data for the cart item.

        Returns:
            CartItem: The created wishlist item.

        Raises:
            Response with 400 status code if something goes wrong while adding the item to the wishlist.

        """
        data = validated_data
        try:
            wishlist_item, created = WishlistItem.objects.get_or_create(**data)

            if created:
                wishlist_item.wishlist.total_price += wishlist_item.product.price
                wishlist_item.wishlist.save()

        except Exception:
            return response.Response(
                {
                    "message": "Something went wrong while adding item to wishlist",
                    "success": False,
                }
            )

        return wishlist_item
