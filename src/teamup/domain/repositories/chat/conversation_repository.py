from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from ...entities import Conversation


class IConversationRepository(ABC):
    @abstractmethod
    async def create(self, conversation: Conversation) -> Optional[Conversation]:
        """
        Создает новую беседу.

        Returns:
            `Optional[Conversation]`: созданная беседу или `None`, если создание не удалось.
        """
        ...

    @abstractmethod
    async def get_by_id(self, conversation_id: UUID) -> Optional[Conversation]:
        """
        Получает беседу по её идентификатору.

        Returns:
            `Optional[Conversation]`: найденная беседу или `None`, если не найдена.
        """
        ...

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> list[Conversation]:
        """
        Получает беседу по идентификатору пользователя.

        Returns:
            `list[Conversation]`: список найденных бесед.
        """
        ...

    @abstractmethod
    async def get_by_announcement_id(self, announcement_id: UUID) -> list[Conversation]:
        """
        Получает беседу по идентификатору объявления.

        Returns:
            `list[Conversation]`: список найденных бесед.
        """
        ...

    @abstractmethod
    async def delete(self, conversation_id: UUID) -> bool:
        """
        Удаляет беседу.

        Returns:
            `bool`: `True`, если удаление прошло успешно, `False` в противном случае.
        """
        ...
