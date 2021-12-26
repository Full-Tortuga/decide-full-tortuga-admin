from rest_framework.exceptions import ValidationError


def is_valid(expression, msg):
    if not expression:
        raise ValidationError(msg)
