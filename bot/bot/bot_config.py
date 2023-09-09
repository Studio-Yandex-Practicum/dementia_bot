from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from core.config import settings

from app.handlers.start_handler import start_router

dp = Dispatcher()
dp.include_router(start_router)

bot = Bot(settings.telegram_api_token, parse_mode=ParseMode.HTML)


def run_webhooks() -> None:
    pass


async def run_polling() -> None:
    await dp.start_polling(bot)
