from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import (SimpleRequestHandler,
                                            setup_application)
from aiohttp import web

from app.handlers.cancel_handler import cancel_router
from app.handlers.test_handler import question_router
from app.handlers.start_handler import start_router
from app.handlers.register_handler import register_router
from core.config import settings

dp = Dispatcher()
dp.include_router(cancel_router)
dp.include_router(start_router)
dp.include_router(register_router)
dp.include_router(question_router)

bot = Bot(settings.telegram_api_token, parse_mode=ParseMode.HTML)


async def run_polling() -> None:
    await dp.start_polling(bot)


async def on_startup(bot: Bot) -> None:
    await bot.set_webhook(f"{settings.BASE_WEBHOOK_URL}"
                          f"{settings.WEBHOOK_PATH}",
                          secret_token=settings.WEBHOOK_SECRET)


def run_webhooks() -> None:
    dp.startup.register(on_startup)
    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=settings.WEBHOOK_SECRET,
    )
    webhook_requests_handler.register(app, path=settings.WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)
    web.run_app(app, host=settings.WEB_SERVER_HOST,
                port=settings.WEB_SERVER_PORT)
