import re
from rest_framework import serializers


def is_valid_password(password):
    """
        Validates the strength of a password based on specific criteria.

        Args:
            password (str): The password to be validated.

        Raises:
            serializers.ValidationError: If the password does not meet the required criteria.

        Note:
            The password must meet the following criteria:
            - Contains at least one uppercase letter
            - Contains at least one lowercase letter
            - Contains at least one numeric digit
            - Contains at least one special character
            - Must be 8 to 15 characters long
            - Cannot contain any whitespace
    """
    regx = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9])(?!.*\s).{8,15}$"
    match_regx = re.compile(regx)

    if not match_regx.match(password):
        raise serializers.ValidationError("Password must contain at least one uppercase letter, one lowercase letter, "
                                          "one number and one special character.")
