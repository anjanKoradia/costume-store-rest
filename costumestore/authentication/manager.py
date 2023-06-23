from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
        Custom manager for the User model. Provides methods for creating users with specified email, password,
        and additional fields.

        Note:
            This manager provides methods for creating regular users and superusers.

        Raises:
            ValueError: If the email field is not provided or if the is_staff or is_superuser fields are not set
                        appropriately for a superuser.
    """
    use_in_migrations = True

    def create(self, email, password=None, **extra_fields):
        """
            Creates a regular user.

            Args:
                email (str): The email address of the user.
                password (str, optional): The password for the user. Defaults to None.
                **extra_fields: Additional fields to be set for the user.

            Returns:
                User: The created User object.

            Raises:
                ValueError: If the email field is not provided.
        """
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
            Creates a superuser.

            Args:
                email (str): The email address of the superuser.
                password (str, optional): The password for the superuser. Defaults to None.
                **extra_fields: Additional fields to be set for the superuser.

            Returns:
                User: The created User object.

            Raises:
                ValueError: If the is_staff or is_superuser fields are not set appropriately for a superuser.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create(email, password, **extra_fields)
