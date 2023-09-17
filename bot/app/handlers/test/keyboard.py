from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

kb_gender = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Мужской'),
            KeyboardButton(text='Женский'),
        ],
    ],
    resize_keyboard=True
)
