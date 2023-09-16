from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


kb_gender = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Мужской'),
            KeyboardButton(text='Женский'),
        ],
    ],
    resize_keyboard=True
)
