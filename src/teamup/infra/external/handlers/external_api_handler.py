from functools import wraps
from typing import Any, Awaitable, Callable, Optional, ParamSpec, cast

from httpx import AsyncClient, ConnectError, ReadError, Response, TimeoutException

from teamup.core import get_logger

logger = get_logger()
P = ParamSpec("P")


class ExternalApiHandler:
    """
    Объект с методами для выполнения HTTP-запросов.
    """

    def __init__(self, client: Optional[AsyncClient] = None):
        self.client = client or AsyncClient()

    @staticmethod
    def req_repeat(
        func: Callable[P, Awaitable[Response]],
    ) -> Callable[P, Awaitable[Optional[Response]]]:
        """
        Функция для повторного выполнения асинхронной функции в случае ошибок.

        Returns:
            `Callable[P, Awaitable[str | None]]`: Функция-обертка для повторного выполнения асинхронной функции в случае ошибок.

        Raises:
            `httpx.TimeoutException: Если превышено время ожидания.
            `httpx.ConnectError`: Если не удалось подключиться к серверу.
            `httpx.ReadError`: Если произошла ошибка при чтении данных.
            `Exception`: Если произошла непредвиденная ошибка.
        """

        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> Optional[Response]:
            for attempt in range(1, 11):
                try:
                    res = await func(*args, **kwargs)
                    if res.status_code >= 200 and res.status_code < 300:
                        return res
                    logger.warning(f"Попытка {attempt}/10: статус {res.status_code}")
                    continue
                except (TimeoutException, ConnectError, ReadError) as e:
                    logger.warning(f"Попытка {attempt}/10: сеть: {e}")
                    continue
                except Exception as e:
                    logger.error(
                        f"Критическая ошибка: {type(e).__name__}: {e}", exc_info=True
                    )
                    return None

            logger.error("Все 10 попыток исчерпаны")
            return None

        return cast(Callable[P, Awaitable[Optional[Response]]], wrapper)

    @req_repeat
    async def get(self, url: str) -> Response:
        return await self.client.get(url)

    @req_repeat
    async def post(self, url: str, json: dict[str, Any]) -> Response:
        return await self.client.post(url, json=json)
