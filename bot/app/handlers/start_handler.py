from aiogram import Router, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, BotCommand
from aiogram.utils.markdown import hbold
from aiogram.enums import ParseMode

from core.config import settings
from app.handlers.handler_constants import START_MESSAGE, BOT_COMMANDS

bot = Bot(settings.telegram_api_token, parse_mode=ParseMode.HTML)

start_router = Router()


@start_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(
        f"Привет, {hbold(message.from_user.full_name)}!"
        f"\n{START_MESSAGE}"
    )
    await bot.set_my_commands(
        commands=[
            BotCommand(
                command=command,
                description=description
            ) for command, description in BOT_COMMANDS.items()
        ],
    )
