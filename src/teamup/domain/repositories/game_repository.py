from abc import abstractmethod
from typing import Optional
from uuid import UUID

from teamup.domain import Game


class IGameRepository:
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
