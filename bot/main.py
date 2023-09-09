import asyncio
import logging
import sys

from bot.bot_config import run_webhooks, run_polling
from core.config import settings


def start() -> None:
    if settings.webhook_mode:
        run_webhooks()
    else:
        asyncio.run(run_polling())


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    start()
