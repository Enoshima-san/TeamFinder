from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from src.teamup.domain import Announcement, Game, User


class IAnnouncementRepository(ABC):
    @abstractmethod
    async def create(self, announcement: Announcement) -> Optional[Announcement]:
        """
        Создаёт запись и возвращает объект анонса.

        Args:
            `announcement` - доменная сущность типа `Announcement` с заполненными полями для создания

        Returns:
            - `Announcement`
            - `None`: если создание не удалось
        """
        pass

    @abstractmethod
    async def delete(self, announcement: Announcement) -> bool:
        """
        Удаляет запись об анонсе при найденном совпадении

        Args:
            `announcement` - доменная сущность анонса

        Returns:
            `True`/`False` - резульат удаления анонса
        """
        pass

    @abstractmethod
    async def get_all(self) -> list[Announcement]:
        """
        Возвращает список всех анонсов.

        Returns:
            `list[Announcement]`: Список доменных объектов
        """
        pass

    @abstractmethod
    async def get_by_id(self, announcement_id: UUID) -> Optional[Announcement]:
        """
        Возвращает анонс по его id.

        Args:
            `announcement_id` - id анонса

        Returns:
            - `Announcement`: доменный объект анонса
            - `None`: если анонс не найден
        """
        pass

    @abstractmethod
    async def get_by_user(self, user: User) -> list[Announcement]:
        pass

    @abstractmethod
    async def get_by_game(self, game: Game) -> list[Announcement]:
        pass

    @abstractmethod
    async def get_all_active_with_relations(
        self,
    ) -> list[tuple[Announcement, User, Game]]:
        """
        Возвращает все активные анонсы с связанными пользователями и играми.

        Returns:
            `list[tuple[Announcement, User, Game]]` - Список всех объявлений с их связями (FK) (кортежи)
        """
        pass

    @abstractmethod
    async def update(self, announcement: Announcement) -> Optional[Announcement]:
        pass
