import re


def validate_birthday(birthday: str):
    """Валидация введенных данных в поле Дата рождения"""
    return re.fullmatch(
        r"^((0[1-9]|[12]\d)\.(0[1-9]|1[012])|"
        r"30\.(0[13-9]|1[012])|31\.(0[13578]|1[02]))\.(19|20)\d\d$",
        birthday
    )


def validate_gender(gender):
    """Валидация введенных данных в поле Пол пользователя"""
    choice = ["Мужской", "Женский"]
    return gender in choice


def validate_bool_answer(answer: str):
    available_answers = ['Да', 'Нет']
    if answer in available_answers:
        return True
    return False

