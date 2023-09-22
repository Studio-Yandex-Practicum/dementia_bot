import re
from datetime import datetime

import botapp.constants as const
from django.core.exceptions import ValidationError


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
