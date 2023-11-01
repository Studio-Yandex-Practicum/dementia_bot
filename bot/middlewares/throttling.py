from typing import Callable, Dict, Awaitable, Any

from aiogram import BaseMiddleware
from aiogram.types import Message
from cachetools import TTLCache


class Throttling(BaseMiddleware):
    """Middleware антиспам с лимитом в переменной limit"""

    def __init__(self, time_limit: int) -> None:
        self.limit = TTLCache(maxsize=10_000, ttl=time_limit)

    async def __call__(
            self,
            handler: Callable[[[Message], Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        if event.chat.id in self.limit:
            await event.answer('Вы слишком часто отправляете сообщения.')
            return
        else:
            self.limit[event.chat.id] = None
        return await handler(event, data)
