from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, \
    InlineKeyboardButton

from app.handlers.test.callback import AnswerCallback, Action, SexCallback, Sex

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
            InlineKeyboardButton(text="Да", callback_data="Да"),
            InlineKeyboardButton(text="Нет", callback_data="Нет")
        ])
    if type == "gender":
        buttons.append([
            InlineKeyboardButton(text="Мужской", callback_data="Мужской"),
            InlineKeyboardButton(text="Женский", callback_data="Женский")
        ])

    markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    return markup

def answer_keyboarder():
    builder = InlineKeyboardBuilder()
    builder.button(
        text=Action.yes,
        callback_data=AnswerCallback(action=Action.yes)
    )
    builder.button(
        text=Action.no,
        callback_data=AnswerCallback(action=Action.no)
    )

    return builder.as_markup()

def sex_keyboarder():
    builder = InlineKeyboardBuilder()
    builder.button(
        text=Sex.male,
        callback_data=SexCallback(action=Sex.male)
    )
    builder.button(
        text=Sex.female,
        callback_data=SexCallback(action=Sex.female)
    )

    return builder.as_markup()

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
