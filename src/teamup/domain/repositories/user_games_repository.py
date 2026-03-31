from abc import abstractmethod
from typing import Optional
from uuid import UUID

from teamup.domain import UserGames


class IUserGamesRepository:
    @abstractmethod
    async def create(self, user_game: UserGames) -> Optional[UserGames]:
        """
        Создает запись и возвращает объект игры пользователя.

        Args:
            `user_game`: предварительно заполненная сущность `UserGames` с установленными вторичными ключами

        Returns:
            - `UserGames`: сущность, хранящая связи (FK) `User` и `Game`
            - `None` при провале операции
        """
        ...

    @abstractmethod
    async def delete(self, user_id: UUID, game_id: UUID) -> bool:
        """
        Удаление игры пользователя.

        Args:
            `user_game`: предварительно заполненная сущность `UserGames` с установленными вторичными ключами

        Returns:
            - `True`/`False`: результат выполнения операции
        """
        ...

    @abstractmethod
    async def get_by_fk(self, user_id: UUID, game_id: UUID) -> Optional[UserGames]:
        """
        Возвращает игру пользователя.

        Args:
            - `user_id`: идентификатор пользователя
            - `game_id`: идентификатор игры

        Returns:
            - `UserGames`: сущность хранящая связи (FK) `User` и `Game`
            - `None`: если совпадений не найдено
        """
        ...

    @abstractmethod
    async def get_all(self, user_id: UUID) -> list[UserGames]:
        """
        Возвращает все игры пользователя, как связи.

        Args:
            - `user_id`: идентификатор пользователя

        Returns:
            - `list[UserGames]`: список сущностей хранящих связи (FK) `User` и `Game`
        """
        ...

    @abstractmethod
    async def get_all_by_user(self, user_id: UUID) -> list[UserGames]:
        """
        Возвращает все игры пользователя.

        Args:
            - `user_id`: идентификатор пользователя

        Returns:
            - `list[UserGames]`: список сущностей хранящих связи (FK) `User` и `Game`
        """
        ...
