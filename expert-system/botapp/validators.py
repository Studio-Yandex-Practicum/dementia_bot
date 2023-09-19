import re
from datetime import datetime

from django.core.exceptions import ValidationError

import botapp.constants as const


def validate_email(email):
    """Функция для валидации email."""

    pattern = const.EMAIL_REGEX

    if not re.match(pattern, email):
        raise ValidationError("Invalid email format")


def validate_dob(dob):
    """Функция для валидации даты рождения."""

    try:
        date_of_birth = datetime.strptime(dob, "%Y-%m-%d").date()
        current_year = datetime.now().year
        age = current_year - date_of_birth.year

        if not (10 <= age <= 100):
            raise ValidationError("Invalid age range")

    except ValueError:
        raise ValidationError("Invalid date format")
