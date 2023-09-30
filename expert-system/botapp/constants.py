QUESTION_TYPES = [
    ('name', 'Имя'),
    ('gender', 'Пол'),
    ('birthdate', 'Дата рождения'),
    ('email', 'Электронная почта'),
    ('occupation', 'Профессия/образование'),
    ('telegram_id', 'ID Telegram'),
    ('text', 'Текст'),
    ('radio', 'Выбор да/нет'),
    ('date', 'Выбор даты'),
    ('text&pictures', 'Текст и картинки'),
    ('buttons', 'Кнопки'),
    ('file', 'Файл'),
    ('drawing', 'Рисунок'),
    ('countries', 'Страны'),
    ('circle', 'Круг'),
    ('triangle', 'Треугольник'),
    ('final', 'Финальный вопрос')
]


GENDER_CHOICES = [
    ('М', 'Мужской'),
    ('Ж', 'Женский'),
]

EMAIL_REGEX = '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]+(?<=.)\S{1,}$'


PERSONAL_DETAILS = ['name', 'birthdate', 'gender',
                    'occupation', 'email', 'telegram_id']


OPTION_CHOICES = (
    ('yes', 'Да'),
    ('no', 'Нет'),
    ('sometimes', 'Иногда'),
    ('male', 'Мужской'),
    ('female', 'Женский'),
)
