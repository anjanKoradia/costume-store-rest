import re
from rest_framework import serializers

def is_valid_password(password):
    regx = "^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9])(?!.*\s).{8,15}$"
    match_regx = re.compile(regx)

    if not match_regx.match(password):
        raise serializers.ValidationError("Password must contain at least one uppercase letter, one lowercase letter, one number and one special character.")