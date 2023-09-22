import urllib.parse
from asyncio import get_event_loop

import aiohttp


class HttpClient:
    """HTTP API клиент."""

    def __init__(self, token=None):
        """Инициализирует клиента."""
        self.token = token
        self.session = aiohttp.ClientSession()

    async def _request(
            self, method, url, data=None, acceptable_statuses=(200,)
            ):
        """Отправляет запрос к API."""
        headers = {}
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'

        async with self.session.request(
            method, url, json=data, headers=headers
        ) as response:
            if response.status not in acceptable_statuses:
                raise Exception(
                    f"Ошибка при отправке запроса: {response.status}"
                )
            return await response.json()

    async def get(self, url, acceptable_statuses=(200,)):
        """Отправляет GET-запрос."""
        return await self._request(
            'GET', url, acceptable_statuses=acceptable_statuses
        )

    async def post(self, url, data, acceptable_statuses=(200, 201, 204)):
        """Отправляет POST-запрос."""
        return await self._request(
            'POST', url, data, acceptable_statuses=acceptable_statuses
        )

    async def patch(self, url, data=None, acceptable_statuses=(200, 201, 204)):
        """Отправляет PATCH-запрос."""
        return await self._request(
            'PATCH', url, data, acceptable_statuses=acceptable_statuses
        )

    @staticmethod
    def _encode_url(url):
        """Кодирует URL, заменяя небезопасные символы на %xx."""
        return urllib.parse.quote(url, safe='')

    async def close(self):
        """Закрывает сессию клиента."""
        await self.session.close()

    async def __aenter__(self):
        """Вход в менеджер контекста."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Выход из менеджера контекста."""
        await self.close()


async def main():
    async with HttpClient() as client:
        response = await client.get('https://example.com/api/data')
        print(response)


if __name__ == "__main__":
    loop = get_event_loop()
    loop.run_until_complete(main())
