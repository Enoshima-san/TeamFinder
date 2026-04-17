from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from ...entities import Notification


class INotificationRepository(ABC):
    @abstractmethod
    async def create(self, notification: Notification) -> Optional[Notification]:
        """
        Создает новое уведомление.

        Returns:
            `Optional[Notification]`: созданное уведомление или `None` в случае ошибки.
        """
        ...

    @abstractmethod
    async def get_by_id(self, notification_id: UUID) -> Optional[Notification]:
        """
        Получает уведомление по идентификатору.

        Returns:
            `Optional[Notification]`: найденное уведомление или `None` если не найдено.
        """
        ...

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> list[Notification]:
        """
        Получает уведомления по идентификатору пользователя.

        Returns:
            `list[Notification]`: список найденных уведомлений.
        """
        ...

    @abstractmethod
    async def get_by_announcement_id(self, announcement_id: UUID) -> list[Notification]:
        """
        Получает уведомления по идентификатору объявления.

        Returns:
            `list[Notification]`: список найденных уведомлений.
        """
        ...

    @abstractmethod
    async def get_by_conversation_id(self, conversation_id: UUID) -> list[Notification]:
        """
        Получает уведомления по идентификатору беседы.

        Returns:
            `list[Notification]`: список найденных уведомлений.
        """
        ...

    @abstractmethod
    async def delete(self, notification_id: UUID) -> bool:
        """
        Удаляет уведомление.

        Returns:
            `bool`: `True` в случае успешного удаления, `False` в случае ошибки.
        """
        ...
