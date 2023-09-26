from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
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

kb_cancel = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Отмена'),
            ],
        ],
        resize_keyboard=True
    )


def inline_builder(tests: list):
    builder = InlineKeyboardBuilder()
    for test in tests:
        builder.button(text=test['title'], callback_data=str(test['id']))
    builder.adjust(1, 1)
    return builder


def markup_keyboard(question_type):
    if question_type == "multiple_choice":
        markup = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Да"),
                    KeyboardButton(text="Нет")
                ],
                [
                    KeyboardButton(text='Отмена'),
                ],
            ],
            resize_keyboard=True
        )
    else:
        markup = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text='Отмена'),
                ],
            ],
            resize_keyboard=True
        )
    return markup
