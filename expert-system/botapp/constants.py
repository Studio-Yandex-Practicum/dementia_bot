TEXT = 'Text Input'

MULTIPLE_CHOICE = 'Yes or no'

PERSONAL = 'Personal question'

QUESTION_TYPES = [
        (TEXT, 'Текст. Ввод информации'),
        (MULTIPLE_CHOICE, 'Выбор да/нет'),
        (PERSONAL, 'Персональные данные'),
    ]

GENDER_CHOICES = (
        ('M', 'Мужчина'),
        ('F', 'Женщина'),
        )

EMAIL_REGEX = '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]+(?<=.)\S{1,}$'
