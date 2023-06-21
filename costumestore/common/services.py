import cloudinary.uploader
from django.conf import settings
from django.core.mail import send_mail


def send_account_activation_email(name, email, email_token):
    subject = "Costumer Store Account Activation"
    email_from = settings.EMAIL_HOST_USER
    message = f"Hi {name.capitalize()}, Click on the link to activate your account http://127.0.0.1:8000/auth/activate/{email_token}"

    send_mail(subject, message, email_from, [email], fail_silently=False)


class CloudinaryServices:
    def store_image(image, folder, tags=[]):
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

    def delete_image(image):
        cloudinary.uploader.destroy(image)
