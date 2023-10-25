from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder

kb_gender = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Мужской'),
            KeyboardButton(text='Женский'),
        ],
    ],
    resize_keyboard=True
)


def finish_test_button():
    return KeyboardButton(text='Завершить тест')


def markup_keyboard(type):
    buttons = []

    if type == "multiple_choice":
        buttons.append([
            KeyboardButton(text="Да"),
            KeyboardButton(text="Нет")
        ])
    if type == "gender":
        buttons.append([
            KeyboardButton(text="Мужской"),
            KeyboardButton(text="Женский")
        ])
    # Добавьте обработку других типов вопросов, для которых нужны кнопки
    if type == "telegram_id":
        # Добавьте обработку типа "telegram_id"
        return ReplyKeyboardRemove()

    markup = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return markup


def prepare_answers(data: dict):
    questions = data.get('questions')
    test_id = data.get('testId')
    json_data = {"testId": test_id,
                 "questions": []}
    for n in range(0, len(questions)):
        answer = {
            "questionId": questions[n]['questionId'],
            "type": questions[n]['type'],
            "answer": data.get(f'answer_{n}')
        }
        json_data['questions'].append(answer)

    return json_data


def inline_builder(tests: list):
    builder = InlineKeyboardBuilder()
    for test in tests:
        builder.button(text=test['title'], callback_data=str(test['id']))
    builder.adjust(1, 1)
    return builder
