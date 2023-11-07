from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from app.handlers.handler_constants import START_MESSAGE
from app.handlers.test.keyboard import inline_builder
from app.handlers.test.states import Question
from core.config import settings
from utils.http_client import HttpClient

start_router = Router()


@start_router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    """
    This handler receives messages with `/start` command
    """
#    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")
    async with HttpClient() as session:
        response = await session.get(
            f'{settings.HOST}api/tests')
    tests = response

    await state.set_state(Question.test)
    await message.answer(
        text=START_MESSAGE,
        reply_markup=inline_builder(tests).as_markup()
    )
