import asyncio
import logging
import sys

from bot.bot_config import run_webhooks, run_polling
from core.config import settings


async def start() -> None:
    if settings.webhook_mode:
        await run_webhooks()
    else:
        await run_polling()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(start())
