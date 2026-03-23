from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository(ABC):
    """Базовый класс для всех репозиториев с поддержкой async context manager."""

    def __init__(self):
        self.session: AsyncSession | None = None

    async def __aenter__(self):
        """Возвращает сам репозиторий при входе в контекст."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Гарантированно закрывает соединение при выходе из контекста."""
        await self.close()

    def check_session(self) -> None:
        if self.session is None:
            raise RuntimeError(
                "Session not initialized. Use 'async with' context manager."
            )

    @abstractmethod
    async def close(self):
        """
        Метод для закрытия ресурсов (сессии БД).
        Должен быть реализован в каждом конкретном репозитории.
        """
        ...
