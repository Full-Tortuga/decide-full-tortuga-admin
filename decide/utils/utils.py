from rest_framework.exceptions import ValidationError


def get_ids(ids):
    return [i for i in ids.split(",") if str.isdigit(i)]


def is_valid(expression, msg):
    if not expression:
        raise ValidationError(msg)
