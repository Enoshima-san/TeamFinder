from abc import abstractmethod
from typing import Optional
from uuid import UUID

from src.teamup.domain import Game

from .base_repository import BaseRepository


class IGameRepository(BaseRepository):
    """
    Работа с "каталогом" игр\n\n
    `Admin only`
    """

    @abstractmethod
    async def create(self, game: Game) -> Optional[Game]: ...

    @abstractmethod
    async def delete(self, game: Game) -> bool: ...

    @abstractmethod
    async def get_all(self) -> list[Game]: ...

    @abstractmethod
    async def get_by_id(self, game_id: UUID) -> Optional[Game]: ...

    @abstractmethod
    async def get_by_name(self, game_name: str) -> Optional[Game]: ...
