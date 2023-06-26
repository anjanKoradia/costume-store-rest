from rest_framework import serializers
from accounts.serializers import AddressSerializer
from django.http import QueryDict
from .models import Order, OrderItem, BillingDetail


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model.

    Attributes:
        - All fields of the Order model.

    Meta:
        - model (Order): The model associated with this serializer.
        - fields (list): The list of fields to include in the serialized representation.
          If set to "__all__", it includes all fields of the model.
    """

    class Meta:
        model = Order
        fields = "__all__"


class OrderItemsSerializer(serializers.ModelSerializer):
    """
    Serializer for the OrderItem model.

    Attributes:
        - All fields of the OrderItem model.

    Methods:
        - get_billing_detail: Get the serialized billing detail associated with the order item.
    """

    billing_detail = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OrderItem
        fields = "__all__"

    def get_billing_detail(self, instance):
        """
        Get the serialized billing detail associated with the order item.

        Args:
            instance (OrderItem): The order item instance.

        Returns:
            dict: The serialized billing detail data.
        """
        serializer = BillingDetailsSerializer(instance.order.billing_detail)
        return serializer.data


class BillingDetailsSerializer(serializers.ModelSerializer):
    """
    Serializer for the BillingDetail model.

    Attributes:
        - All fields of the BillingDetail model.
        - order_item: List of Items associated with this BillingDetail

    Methods:
        - get_order_item: Get the serialized order items associated with the billing detail.
        - to_internal_value: Convert the incoming data to its internal form.
        - create: Create a new billing detail.
    """

    order_item = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = BillingDetail
        fields = "__all__"

    def get_order_item(self, instance):
        """
        Get the serialized order items associated with the billing detail.

        Args:
            instance (BillingDetail): The billing detail instance.

        Returns:
            dict: The serialized order item data.
        """
        return instance.order.items.all().values()

    def to_internal_value(self, data):
        """
        Convert the incoming data to its internal form.

        Args:
            data (dict): The data to convert.

        Returns:
            dict: The converted internal value representation of the data.

        Raises:
            ValueError: If the user's cart is empty.

        """
        user = self.context["request"].user

        if len(user.cart.items.all()) == 0:
            raise ValueError("Cart is empty")

        order_serializer = OrderSerializer(
            data={
                "user": user.id,
                "amount": user.cart.total_price,
                "order_note": data["order_note"],
            }
        )
        if order_serializer.is_valid():
            order = order_serializer.save()
        else:
            return order_serializer.errors

        address_serializer = AddressSerializer(
            data={
                "address": data["address"],
                "pin_code": data["pin_code"],
                "city": data["city"],
                "state": data["state"],
                "country": data["country"],
                "type": "billing",
            },
            context={"request": self.context["request"]},
        )
        if address_serializer.is_valid():
            address = address_serializer.save()
        else:
            return address_serializer.errors

        params = {
            "order": order.id,
            "name": data["name"],
            "address": address.id,
            "phone": data["phone"],
            "email": data["email"],
        }
        query_dict = QueryDict("", mutable=True)
        query_dict.update(params)

        return super().to_internal_value(query_dict)

    def create(self, validated_data):
        """
        Create a new billing detail.

        Args:
            validated_data (dict): The validated data for the billing detail.

        Returns:
            BillingDetail: The created billing detail.

        """
        data = validated_data
        user = self.context["request"].user

        for item in user.cart.items.all():
            OrderItem.objects.create(
                order=data["order"],
                product=item.product,
                quantity=item.quantity,
                size=item.size,
                color=item.color,
            )

        billing_details = BillingDetail.objects.create(
            order=data["order"],
            name=data["name"],
            address=data["address"],
            phone=data["phone"],
            email=data["email"],
        )
        user.cart.items.all().delete()

        return billing_details
