from common import models, services
from rest_framework import response, serializers
from .models import Product, ProductImage


class ColorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Color model.

    This serializer is responsible for serializing and deserializing Color objects.

    Attributes:
        model (Color): The Color model class.
        fields (list): The list of fields to include in the serialized representation.

    Methods:
    to_representation(instance): Customizes the serialized representation of Color instances. And return
                                 list of colors
    create(validated_data): Creates a new Color instance and associates it with a product.
                            colors object is created else false
    """

    class Meta:
        model = models.Color
        fields = ["name"]

    def to_representation(self, instance):
        return instance.name

    def create(self, validated_data):
        data = validated_data
        product = self.context["product"]

        instance, created = models.Color.objects.get_or_create(name=data.get("name"))
        product.colors.add(instance)
        return created


class SizeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Size model.

    Attributes:
        Meta (class): Metadata options for the serializer.
            - model (Model): The Size model associated with the serializer.
            - fields (list): The fields to include in the serialized representation.

    Methods:
        to_representation(instance): Converts the instance to a serialized representation. And return list of sizes
        create(validated_data): Creates a new Size instance and associates it with a product. And return true if
                                the size object is created else false
    """

    class Meta:
        model = models.Size
        fields = ["name"]

    def to_representation(self, instance):
        return instance.name

    def create(self, validated_data):
        data = validated_data
        product = self.context["product"]

        instance, created = models.Size.objects.get_or_create(name=data.get("name"))
        product.sizes.add(instance)
        return created


class ProductImageSerializer(serializers.Serializer):
    """
    Serializer for handling product image data.

    Attributes:
        image (serializers.ImageField): The product image field.
        url (serializers.URLField): The URL field for the image.

    Methods:
        to_representation(instance): Convert the instance to its representation. And return list of image urls
        create(validated_data): Create a new product image instance,store images in cloudinary
    """

    image = serializers.ImageField(required=True, write_only=True)
    url = serializers.URLField(read_only=True)

    def to_representation(self, instance):
        return instance.url

    def create(self, validated_data):
        data = validated_data
        product = self.context["product"]
        user = self.context["user"]

        try:
            image = services.CloudinaryServices.store_image(
                data.get("image"),
                "Products/" + user.vendor.shop_name + "/" + product.name + "/images",
                [product.category, product.subcategory],
            )

            ProductImage.objects.create(
                product=product,
                url=image["url"],
                public_id=image["public_id"],
            )
        except Exception:
            return response.Response(
                {
                    "message": "Something went wrong while uploading images.",
                    "success": False,
                }
            )
        return product


class GetProductSerializer(serializers.ModelSerializer):
    """
     Serializer for retrieving product information.

    Attributes:
         sizes (SizeSerializer): Serializer for sizes associated with the product.
         colors (ColorSerializer): Serializer for colors associated with the product.
         product_images (ProductImageSerializer): Serializer for images of the product.

    Meta:
         model (Product): The model class to be serialized.
         exclude (List[str]): Fields to be excluded from serialization.
    """

    sizes = SizeSerializer(many=True)
    colors = ColorSerializer(many=True)
    product_images = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        exclude = ["vendor"]


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the 'Product' model.

    Attributes:
        sizes (ListField): List of sizes associated with the product.
        colors (ListField): List of colors associated with the product.
        images (ListField): List of images associated with the product.

    Meta:
        model (Product): The model class to serialize.
        exclude (list): Fields to exclude from the serialized representation.

    Methods:
        to_representation(instance): Custom representation of the serialized data. And return list of product data
        create(validated_data): Create and store a new product instance. And return that product instance
        update(instance, validated_data): Update an existing product instance and return updated product instance
    """

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
        except Exception:
            return response.Response(
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
