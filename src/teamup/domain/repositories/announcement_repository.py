from abc import abstractmethod
from typing import Optional
from uuid import UUID

from teamup.domain import Announcement, Game, User

from .base import BaseRepository


class IAnnouncementRepository(BaseRepository):
    @abstractmethod
    async def create(self, announcement: Announcement) -> Optional[Announcement]:
        """
        Создаёт объявление.

        Args:
            `announcement`: доменная сущность типа `Announcement` с заполненными полями для создания

        Returns:
            - `Announcement`
            - `None`: если создание не удалось
        """
        ...

    @abstractmethod
    async def delete(self, announcement_id: UUID) -> bool:
        """
        Удаляет запись об анонсе при найденном совпадении

        Args:
            `announcement`: доменная сущность анонса

        Returns:
            `True`/`False`: резульат удаления анонса
        """
        ...

    @abstractmethod
    async def get_all(self) -> list[Announcement]:
        """
        Возвращает список всех анонсов.

        Returns:
            `list[Announcement]`: Список доменных объектов
        """
        ...

    @abstractmethod
    async def get_by_id(self, announcement_id: UUID) -> Optional[Announcement]:
        """
        Возвращает анонс по его id.

        Args:
            `announcement_id`: id анонса

        Returns:
            - `Announcement`: доменный объект анонса
            - `None`: если анонс не найден
        """
        ...

    @abstractmethod
    async def get_by_id_with_relations(
        self, announcement_id: UUID
    ) -> Optional[tuple[Announcement, User, Game]]:
        """
        Возвращает анонс по его id с его отношениями.

        Args:
            `announcement_id`: id анонса

        Returns:
            - `tuple[Announcement, User, Game]`: Доменный объект анонса с его связямя
            - `None`: Если анонс не найден
        """
        ...

    @abstractmethod
    async def get_by_user(self, user: User) -> list[Announcement]: ...

    @abstractmethod
    async def get_by_game(self, game: Game) -> list[Announcement]: ...

    @abstractmethod
    async def get_all_active_with_relations(
        self,
    ) -> list[tuple[Announcement, User, Game]]:
        """
        Возвращает все активные анонсы с связанными пользователями и играми.

        Returns:
            `list[tuple[Announcement, User, Game]]`: Список всех объявлений с их связями (FK) (кортежи)
        """
        ...

    @abstractmethod
    async def update(self, announcement: Announcement) -> Optional[Announcement]: ...
