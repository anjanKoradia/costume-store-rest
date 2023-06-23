import uuid
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from rest_framework import status
from rest_framework.response import Response
from authentication.models import User
from cart.models import Cart, CartItem
from wishlist.models import Wishlist, WishlistItem
from .models import Image
from .services import CloudinaryServices, send_account_activation_email


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Signal receiver function to send activation mail after creating a profile

    Args:
        sender (Model): The model class that sent the signal (User).
        instance (User): The actual instance of the User model.
        created (bool): Indicates if the User instance was created or updated.
    """
    if created:
        try:
            user = User.objects.get(email=instance.email)
        except User.DoesNotExist:
            return Response(
                {"message": "User not found.", "success": False},
                status=status.HTTP_404_NOT_FOUND,
            )

        email_token = str(uuid.uuid4())
        user.email_token = email_token
        user.save()

        if instance.role == "customer":
            Cart.objects.create(user=instance)
            Wishlist.objects.create(user=instance)

        send_account_activation_email(instance.name, instance.email, email_token)


@receiver(post_delete, sender=Image)
def delete_image(sender, instance, **kwargs):
    """
    Signal receiver function to delete an image from Cloudinary after Image model is deleted.

    Args:
        sender (Model): The model class that sent the signal (Image).
        instance (Image): The actual instance of the Image model.
    """
    CloudinaryServices.delete_image(image=instance.public_id)


@receiver(post_save, sender=CartItem)
def delete_cart_item(sender, instance, created, **kwargs):
    """
    Signal receiver to delete the cart item if its quantity is set to 0.

    Args:
        sender (Model): The model class that sent the signal (CartItem).
        instance (CartItem): The actual instance of the CartItem model.
    """
    if not created:
        if instance.quantity == 0:
            CartItem.objects.get(id=instance.id).delete()


@receiver(post_delete, sender=CartItem)
def update_cart(sender, instance, **kwargs):
    """
    Signal receiver to update the cart's total price when a cart item is deleted.

    Args:
        sender (Model): The model class that sent the signal (CartItem).
        instance (CartItem): The actual instance of the CartItem model.
    """
    cart = instance.cart
    cart.total_price -= instance.product.price * instance.quantity
    cart.save()


@receiver(post_delete, sender=WishlistItem)
def update_wishlist(sender, instance, **kwargs):
    """
    Signal receiver to update the wishlist price when a wishlist item is deleted.

    Args:
        sender (Model): The model class that sent the signal (WishlistItem).
        instance (WishlistItem): The actual instance of the WishlistItem model.
    """
    wishlist = instance.wishlist
    wishlist.total_price -= instance.product.price
    wishlist.save()
