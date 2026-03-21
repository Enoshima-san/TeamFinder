from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from src.teamup.domain import Game


class IGameRepository(ABC):
    """
    Работа с "каталогом" игр\n\n
    `Admin only`
    """

    @abstractmethod
    async def create(self, game: Game) -> Optional[Game]:
        pass

    @abstractmethod
    async def delete(self, game: Game) -> bool:
        pass

    @abstractmethod
    async def get_all(self) -> list[Game]:
        pass

    @abstractmethod
    async def get_by_id(self, game_id: UUID) -> Optional[Game]:
        pass

    @abstractmethod
    async def get_by_name(self, game_name: str) -> Optional[Game]:
        pass
