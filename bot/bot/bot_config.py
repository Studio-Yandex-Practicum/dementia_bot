from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import (SimpleRequestHandler,
                                            setup_application)
from aiogram.types import BotCommand


from aiohttp import web
from app.handlers.question_handler import question_router
from app.handlers.start_handler import start_router
from app.handlers.test_handler import form_router
from app.handlers.handler_constants import (
    BOT_SHORT_DESCRIPTION,
    BOT_LONG_DESCRIPTION,
    BOT_COMMANDS,
)
from core.config import settings

dp = Dispatcher()
dp.include_router(start_router)
dp.include_router(form_router)
dp.include_router(question_router)

bot = Bot(settings.telegram_api_token, parse_mode=ParseMode.HTML)


async def set_commands() -> None:
    await bot.set_my_commands(
        commands=[
            BotCommand(
                command=command,
                description=description
            ) for command, description in BOT_COMMANDS.items()
        ],
    )


async def set_description() -> None:
    await bot.set_my_description(BOT_LONG_DESCRIPTION)
    await bot.set_my_short_description(BOT_SHORT_DESCRIPTION)


async def run_polling() -> None:
    await dp.start_polling(bot)
    await set_description()
    await set_commands()


async def on_startup(bot: Bot) -> None:
    await bot.set_webhook(f"{settings.BASE_WEBHOOK_URL}"
                          f"{settings.WEBHOOK_PATH}",
                          secret_token=settings.WEBHOOK_SECRET)
    await set_description()
    await set_commands()


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
