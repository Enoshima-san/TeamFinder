from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from ...entities import Message


class IMessageRepository(ABC):
    @abstractmethod
    async def create(self, message: Message) -> Optional[Message]:
        """
        Создаёт сообщение.

        Returns:
            `Optional[Message]`: созданное сообщение или `None`, если создание не удалось.
        """
        ...

    @abstractmethod
    async def get_by_conversation_id(self, conversation_id: UUID) -> list[Message]:
        """
        Получает все сообщения по идентификатору беседы.

        Returns:
            `list[Message]`: список сообщений.
        """
        ...

    @abstractmethod
    async def get_by_id(self, message_id: UUID) -> Optional[Message]:
        """
        Получает сообщение по его идентификатору.

        Returns:
            `Optional[Message]`: сообщение или `None`, если сообщение не найдено.
        """
        ...

    @abstractmethod
    async def soft_delete(self, message_id: UUID) -> bool:
        """
        Устанавливает статус "удалено" для сообщения.

        Returns:
            `bool`: `True`, если удаление прошло успешно, `False` в противном случае.
        """
        ...

    @abstractmethod
    async def delete(self, message_id: UUID) -> bool:
        """
        Удаляет сообщение.

        Returns:
            `bool`: `True`, если удаление прошло успешно, `False` в противном случае.
        """
        ...
