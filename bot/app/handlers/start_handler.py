from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import link
from aiogram.enums import ParseMode

from app.handlers.handler_constants import (
    START_MESSAGE,
    PROJECT_LINK,
    PROJECT_LINK_TITLE,
)

start_router = Router()


@start_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(
        "На связи команда проекта "
        f"{link(title=PROJECT_LINK_TITLE, url=PROJECT_LINK)}\!"
        f"\n{START_MESSAGE}", parse_mode=ParseMode.MARKDOWN_V2
    )
