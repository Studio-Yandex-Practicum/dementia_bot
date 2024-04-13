from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, WebAppInfo, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.handlers.handler_constants import (
    ABOUT_TEST_TEXT, HELP_TEST_TEXT, TEST_URL
)


form_router = Router()


@form_router.message(Command('test'))
async def test(message: Message) -> None:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text='Тестирование', callback_data='test')
    )
    await message.answer(
        text=ABOUT_TEST_TEXT,
        reply_markup=builder.as_markup(resize_keyboard=True),
    )


@form_router.callback_query(F.data == "test")
async def test_callback(call: Message) -> None:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text='Проверить себя',
            web_app=WebAppInfo(url=f'{TEST_URL}')
        )
    )
    await call.message.answer(
        text=HELP_TEST_TEXT,
        reply_markup=builder.as_markup(resize_keyboard=True),
    )
