from rest_framework import serializers, response
from .models import CartItem, Cart


class CartSerializer(serializers.ModelSerializer):
    """
    Serializer for the CartItem model.

    Attributes:
        - All fields of the CartItem model.

    Methods:
        - create: Create a new cart item or update an existing one.
        - update: Update the quantity of a cart item based on the specified operation.
    """

    class Meta:
        model = CartItem
        exclude = ["cart"]

    def create(self, validated_data):
        """
        Create a new cart item or update an existing one.

        Args:
            validated_data (dict): The validated data for the cart item.

        Returns:
            CartItem: The created or updated cart item.

        Raises:
            Response with 400 status code if something goes wrong while adding the item to the cart.

        """
        data = validated_data
        quantity = data.pop("quantity")
        user = self.context["request"].user

        try:
            cart, created = Cart.objects.get_or_create(user=user)

            cart_item, created = CartItem.objects.get_or_create(
                **data,
                cart=cart,
                defaults={"quantity": quantity},
            )

            cart_item.cart.total_price += cart_item.product.price * cart_item.quantity
            cart_item.cart.save()

            if not created:
                cart_item.quantity = cart_item.quantity + quantity
                cart_item.save()

        except Exception:
            return response.Response(
                {
                    "message": "Something went wrong while adding item to cart",
                    "success": False,
                }
            )

        return cart_item

    def update(self, instance, validated_data):
        """
        Update the quantity of a cart item based on the specified operation.

        Args:
            instance (CartItem): The cart item instance to update.
            validated_data (dict): The validated data for the update.

        Returns:
            CartItem: The updated cart item.
        """
        url_params = self.context.get("view").kwargs
        operation = url_params.get("operation")

        if operation == "decrease":
            instance.cart.total_price -= instance.product.price
            instance.cart.save()
            instance.quantity -= 1
            instance.save()

        if operation == "increase":
            instance.cart.total_price += instance.product.price
            instance.cart.save()
            instance.quantity += 1
            instance.save()

        return instance
