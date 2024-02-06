import re
from datetime import datetime

import botapp.constants as const
from django.core.exceptions import ValidationError
from botapp.constants import IMAGE_TYPE, IMAGE_SIZE


def validate_email(email):
    """Функция для валидации email."""

    pattern = const.EMAIL_REGEX

    if not re.match(pattern, email):
        raise ValidationError("неверный формат электронной почты")


def validate_dob(dob):
    """Функция для валидации даты рождения."""

    try:
        date_of_birth = datetime.strptime(dob, "%Y-%m-%d").date()
        current_year = datetime.now().year
        age = current_year - date_of_birth.year

        if not (10 <= age <= 100):
            raise ValidationError("Неверный возраст.")

    except ValueError:
        raise ValidationError("Неверный формат даты")


def validate_image(value):

    if value.size/1024 > IMAGE_SIZE:
        raise ValidationError(f"Image size should be less than {IMAGE_SIZE} KB")

    if value.content_type not in IMAGE_TYPE:
        raise ValidationError(f"Image format should be {', '.join(IMAGE_TYPE)}")
