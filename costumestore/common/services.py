import cloudinary.uploader
from django.conf import settings
from django.core.mail import send_mail


def send_account_activation_email(name, email, email_token):
    """
        Sends an account activation email to a user.

        Args:
            name (str): The name of the recipient.
            email (str): The email address of the recipient.
            email_token (str): The unique token for account activation.
    """
    subject = "Costumer Store Account Activation"
    email_from = settings.EMAIL_HOST_USER
    message = f"Hi {name.capitalize()}, " \
              f"Click on the link to activate your account http://127.0.0.1:8000/auth/activate/{email_token}"

    send_mail(subject, message, email_from, [email], fail_silently=False)


class CloudinaryServices:
    """
        Utility class for interacting with Cloudinary image storage service.

        Methods:
            store_image(image, folder, tags=None): Uploads an image to Cloudinary.
            delete_image(image): Deletes an image from Cloudinary.
    """
    def store_image(self, image, folder, tags=None):
        """
            Uploads an image to Cloudinary.

            Args:
                image: The image file to upload.
                folder (str): The destination folder in Cloudinary.
                tags (Optional[List[str]]): Additional tags to associate with the image.

            Returns:
                dict: A dictionary containing the URL and public ID of the uploaded image.

            Raises:
                cloudinary.exceptions.Error: If an error occurs during the upload process.
        """
        result = cloudinary.uploader.upload(
            image,
            folder=folder,
            tags=tags,
        )

        result_dict = {
            "url": result["url"],
            "public_id": result["public_id"],
        }

        return result_dict

    def delete_image(self, image):
        """
            Deletes an image from Cloudinary.

            Args:
                image (str): The public ID of the image to delete.

            Raises:
                cloudinary.exceptions.Error: If an error occurs during the deletion process.
        """
        cloudinary.uploader.destroy(image)
