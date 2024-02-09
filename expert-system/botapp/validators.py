from django.core.exceptions import ValidationError
from botapp.constants import IMAGE_TYPE, IMAGE_SIZE


def validate_image(value):

    if value.size/1024 > IMAGE_SIZE:
        raise ValidationError(f"Image size should be less than {IMAGE_SIZE} KB")

    if value.content_type not in IMAGE_TYPE:
        raise ValidationError(f"Image format should be {', '.join(IMAGE_TYPE)}")
