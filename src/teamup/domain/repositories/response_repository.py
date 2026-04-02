from abc import abstractmethod
from typing import Optional
from uuid import UUID

from teamup.domain import Response


class IResponseRepository:
    @abstractmethod
    async def create(self, response: Response) -> Optional[Response]:
        """
        Создаёт запись и возвращает объект запроса пользователя.

        Args:
            `response`: доменная сущность запроса пользователя

        Returns:
            - `Response`
            - `None`: при неудачной операции
        """
        ...

    @abstractmethod
    async def delete(self, response: Response) -> bool:
        """
        Удаляет запись о запросе при найденном совпадении.

        Args:
            `response`: доменная сущность запроса пользователя

        Returns:
            `True`/`False`: резульат удаления запроса
        """
        ...

    @abstractmethod
    async def update(self, response: Response) -> Optional[Response]:
        """
        Обновляет статус запроса на `принят`/`отклонен`.

        Args:
            `response`: доменная сущность запроса пользователя

        Returns:
            - `Response`
            - `None`: при неудачной операции
        """
        ...

    @abstractmethod
    async def get_by_user(self, user_id: UUID) -> list[Response]:
        """
        Args:
            `user_id`: id пользователя

        Returns:
            `list[Response]`: список всех запросов пользователя
        """
        ...

    @abstractmethod
    async def get_by_announcement(self, announcement_id: UUID) -> list[Response]:
        """
        Args:
            `announcement_id`: id объявления

        Returns:
            - `list[Response]`: список всех запросов на объявление
        """
        ...
