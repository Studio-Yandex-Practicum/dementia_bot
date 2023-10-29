QUESTION_TYPES = [
    ('name', 'Имя'),
    ('gender', 'Пол'),
    ('birthdate', 'Дата рождения'),
    ('email', 'Электронная почта'),
    ('occupation', 'Профессия/образование'),
    ('telegram_id', 'ID Telegram'),
    ('question', 'Текст'),
    ('multiple_choice', 'Выбор да/нет'),
]

OK = 'OK'
DEVIATIONS='DEVIATIONS'
DEMENTIA='DEMENTIA'
NOTEND='NOTEND'

RESULT_CHOISES = [
    (OK, 'Тест пройден успешно'),
    (DEVIATIONS, 'Есть отклонения'),
    (DEMENTIA, 'Деменция'),
    (NOTEND, 'Не закончил тест'),
]


GENDER_CHOICES = [
    ('М', 'Мужской'),
    ('Ж', 'Женский'),
]

EMAIL_REGEX = '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]+(?<=.)\S{1,}$'


PERSONAL_DETAILS = ['name', 'birthdate', 'gender',
                    'occupation', 'email', 'telegram_id']

COUNTRIES = [
    "Австралия",
    "Австрия",
    "Азербайджан",
    "Албания",
    "Алжир",
    "Ангола",
    "Андорра",
    "Антигуа и Барбуда",
    "Аргентина",
    "Армения",
    "Афганистан",
    "Багамы",
    "Бангладеш",
    "Барбадос",
    "Бахрейн",
    "Беларусь",
    "Белиз",
    "Бельгия",
    "Бенин",
    "Болгария",
    "Боливия",
    "Босния и Герцеговина",
    "Ботсвана",
    "Бразилия",
    "Бруней",
    "Буркина-Фасо",
    "Бурунди",
    "Бутан",
    "Вануату",
    "Ватикан",
    "Великобритания",
    "Венгрия",
    "Венесуэла",
    "Вьетнам",
    "Габон",
    "Гаити",
    "Гайана",
    "Гамбия",
    "Гана",
    "Гватемала",
    "Гвинея",
    "Гвинея-Бисау",
    "Германия",
    "Гондурас",
    "Гренада",
    "Греция",
    "Грузия",
    "Дания",
    "Джибути",
    "Доминика",
    "Доминиканская Республика",
    "Египет",
    "Замбия",
    "Зимбабве",
    "Израиль",
    "Индия",
    "Индонезия",
    "Иордания",
    "Ирак",
    "Иран",
    "Ирландия",
    "Исландия",
    "Испания",
    "Италия",
    "Йемен",
    "Кабо-Верде",
    "Казахстан",
    "Камбоджа",
    "Камерун",
    "Канада",
    "Катар",
    "Кения",
    "Кипр",
    "Киргизия",
    "Кирибати",
    "Китай",
    "Колумбия",
    "Коморы",
    "Конго",
    "Коста-Рика",
    "Кот-д'Ивуар",
    "Куба",
    "Кувейт",
    "Лаос",
    "Латвия",
    "Лесото",
    "Либерия",
    "Ливан",
    "Ливия",
    "Литва",
    "Лихтенштейн",
    "Люксембург",
    "Маврикий",
    "Мавритания",
    "Мадагаскар",
    "Малави",
    "Малайзия",
    "Мали",
    "Мальдивы",
    "Мальта",
    "Марокко",
    "Маршалловы Острова",
    "Мексика",
    "Микронезия",
    "Мозамбик",
    "Молдавия",
    "Монако",
    "Монголия",
    "Мьянма",
    "Намибия",
    "Науру",
    "Непал",
    "Нигер",
    "Нигерия",
    "Нидерланды",
    "Никарагуа",
    "Новая Зеландия",
    "Норвегия",
    "Объединенные Арабские Эмираты",
    "Оман",
    "Пакистан",
    "Палау",
    "Панама",
    "Папуа — Новая Гвинея",
    "Парагвай",
    "Перу",
    "Польша",
    "Португалия",
    "Россия",
]
