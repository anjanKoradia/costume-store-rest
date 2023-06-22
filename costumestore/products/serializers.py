from common.models import Color, Size
from rest_framework import serializers
from products.models import ProductImages
from django.db.utils import DatabaseError
from .models import Product, ProductImages
from cloudinary.exceptions import BadRequest
from common.services import CloudinaryServices
from rest_framework.exceptions import ValidationError


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ["name"]

    def to_representation(self, instance):
        return instance.name

    def create(self, validated_data):
        data = validated_data
        product = self.context["product"]

        instance, created = Color.objects.get_or_create(name=data.get("name"))
        product.colors.add(instance)
        return product


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ["name"]

    def to_representation(self, instance):
        return instance.name

    def create(self, validated_data):
        data = validated_data
        product = self.context["product"]

        instance, created = Size.objects.get_or_create(name=data.get("name"))
        product.sizes.add(instance)
        return product


class ProductImageSerializer(serializers.Serializer):
    image = serializers.ImageField(required=True, write_only=True)
    url = serializers.URLField(read_only=True)

    def to_representation(self, instance):
        return instance.url

    def create(self, validated_data):
        data = validated_data
        product = self.context["product"]
        user = self.context["user"]

        try:
            image = CloudinaryServices.store_image(
                data.get("image"),
                "Products/" + user.vendor.shop_name + "/" + product.name + "/images",
                [product.category, product.subcategory],
            )

            ProductImages.objects.create(
                product=product,
                url=image["url"],
                public_id=image["public_id"],
            )
        except BadRequest as e:
            raise ValidationError("Something went wrong while uploading images.")

        return product


class GetProductSerializer(serializers.ModelSerializer):
    sizes = SizeSerializer(many=True)
    colors = ColorSerializer(many=True)
    product_images = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        exclude = ["vendor"]


class ProductSerializer(serializers.ModelSerializer):
    sizes = serializers.ListField(
        child=serializers.CharField(max_length=20), write_only=True
    )
    colors = serializers.ListField(
        child=serializers.CharField(max_length=20), write_only=True
    )
    images = serializers.ListField(child=serializers.ImageField(), write_only=True)

    class Meta:
        model = Product
        exclude = ["vendor"]

    def to_representation(self, instance):
        serializer = GetProductSerializer(instance)
        return serializer.data

    def create(self, validated_data):
        data = validated_data
        user = self.context["request"].user

        try:
            product = Product.objects.create(
                vendor=user.vendor,
                name=data["name"],
                category=data["category"],
                subcategory=data["subcategory"],
                rating=data["rating"],
                price=data["price"],
                discount=data["discount"],
                stock=data["stock"],
                description=data["description"],
            )

            color_data = list(map(lambda color: {"name": color}, data["colors"]))
            color_serializer = ColorSerializer(
                data=color_data, many=True, context={"product": product}
            )
            if color_serializer.is_valid():
                color_serializer.save()
            else:
                raise serializers.ValidationError(color_serializer.errors)

            size_data = list(map(lambda size: {"name": size}, data["sizes"]))
            size_serializer = SizeSerializer(
                data=size_data, many=True, context={"product": product}
            )
            if size_serializer.is_valid():
                size_serializer.save()
            else:
                raise serializers.ValidationError(size_serializer.errors)

            image_data = list(map(lambda img: {"image": img}, data["images"]))
            image_serializer = ProductImageSerializer(
                data=image_data, many=True, context={"product": product, "user": user}
            )
            if image_serializer.is_valid():
                image_serializer.save()
            else:
                raise serializers.ValidationError(size_serializer.errors)

        except DatabaseError as e:
            raise ValidationError(
                {
                    "message": "Something went wrong while storing product details",
                    "success": False,
                }
            )

        return product

    def update(self, instance, validated_data):
        Product.objects.get(id=instance.id).delete()
        product = self.create(validated_data)
        return product
