from abc import abstractmethod
from typing import Optional
from uuid import UUID

from teamup.domain import User

from .base import BaseRepository


class IUserRepository(BaseRepository):
    @abstractmethod
    async def create(self, user: User) -> Optional[User]:
        """
        Создаёт запись и возвращает объект пользователя. Проверяет уникальность email и имени пользователя.

        Args:
            `user`: доменная сущность пользователя

        Returns:
            - `User`
            - `None`: если пользователь уже в базе
        """
        ...

    @abstractmethod
    async def delete(self, user_id: UUID) -> bool:
        """
        Удалаяет запись о пользователе при найденном совпадении.

        Args:
            `user`: доменная сущность пользователя

        Returns:
            `True`/`False`: результат удаления пользователя
        """
        ...

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        """
        Возвращает пользователя и его связи по его id.

        Args:
            `user_id`: id пользователя

        Returns:
            - `User`
            - `None`: если пользователь не найден
        """
        ...

    async def get_by_id_light(self, user_id: UUID) -> Optional[User]:
        """
        Возвращает пользователя по его id.

        Args:
            `user_id`: id пользователя

        Returns:
            - `User`
            - `None`: если пользователь не найден
        """
        ...

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """
        Ищет пользователя по его email.

        Args:
            `email`: email пользователя

        Returns:
            - `User`
            - `None`: если пользователь не найден
        """
        ...

    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[User]:
        """
        Ищет пользователя по его имени в системе.

        Args:
            `username`: уникальное имя пользователя в системе

        Returns:
            - `User`
            - `None`: если пользователь не найден
        """
        ...

    @abstractmethod
    async def get_all(self) -> list[User]:
        """
        Возвращает список всех пользователей в системе.

        Returns:
             list[`User`]: Список доменных объектов
        """
        ...

    @abstractmethod
    async def update(self, user: User) -> Optional[User]:
        """
        Обновляет данные пользователя в системе.

        Args:
            `user`: доменный объект `User` с обновлёнными данными

        Returns:
            - `User`: обновлённый доменный объект
            - `None`: если пользователь не найден
        """
        ...

    @abstractmethod
    async def check_new_user(self, email: str, username: str) -> bool:
        """
        Проверяет возможно ли создать пользователя с введёнными ими данными.\n

        Args:
            - `email`: электронная почта (уникальное поле в БД)
            - `username`: имя пользователя внутри системы (уникальное поле в БД)

        Returns:
            `True`/`False`: результат проверки
        """
        ...

    @abstractmethod
    async def update_password(self, email: str, hashed_password: str) -> Optional[User]:
        """
        Обновляет пароль пользователя в системе.

        Args:
            - `email`: электронная почта пользователя
            - `hashed_password`: хеш нового пароля

        Returns:
            - `User`: обновлённый доменный объект
            - `None`: если пользователь не найден
        """
        ...
