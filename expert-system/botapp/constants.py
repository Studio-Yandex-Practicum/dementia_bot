QUESTION_TYPES = [
    ('name', 'Имя'),
    ('gender', 'Пол'),
    ('birthdate', 'Дата рождения'),
    ('email', 'Электронная почта'),
    ('occupation', 'Профессия/образование'),
    ('telegram_id', 'ID Telegram'),
    ('text', 'Текст'),
    ('multiple_choice', 'Выбор да/нет'),
]


GENDER_CHOICES = [
    ('М', 'Мужской'),
    ('Ж', 'Женский'),
]

EMAIL_REGEX = '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]+(?<=.)\S{1,}$'


PERSONAL_DETAILS = ['name', 'birthdate', 'gender',
                    'occupation', 'email', 'telegram_id']
