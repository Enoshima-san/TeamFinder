from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from teamup.core import get_logger
from teamup.domain import (
    IMessageRepository,
    Message,
)

from ...database.mappers import MessageMapper
from ...database.models.chat import MessageORM


class MessageRepository(IMessageRepository):
    def __init__(self, session: AsyncSession):
        self.logger = get_logger()
        self.session = session
        self.logger.info("Инициализация MessageRepository")

    async def create(self, message: Message) -> Optional[Message]:
        try:
            if message.sender_id == message.recipient_id:
                self.logger.error(
                    "Ошибка при создании сообщения: отправитель и получатель совпадают."
                )
                return None
            orm = MessageMapper.to_orm(message)
            self.session.add(orm)
            await self.session.commit()
            await self.session.refresh(orm)
            self.logger.info("Сообщение сохранено в сессии.")
            return MessageMapper.to_domain(orm)
        except IntegrityError:
            self.logger.error(
                f"Ошибка при создании сообщения пользователя с ID:{message.sender_id}."
            )
            await self.session.rollback()
            return None

    async def get_by_id(self, message_id: UUID) -> Optional[Message]:
        message = await self.session.get(MessageORM, message_id)
        if message is None:
            self.logger.warning(f"Сообщение с  ID:{message_id} не найдено.")
            return None
        self.logger.info(f"Запрос на получение сообщения с ID:{message_id}")
        return MessageMapper.to_domain(message)

    async def get_by_conversation_id(self, conversation_id: UUID) -> list[Message]:
        stmt = (
            select(MessageORM)
            .where(MessageORM.conversation_id == conversation_id)
            .order_by(MessageORM.created_at.desc())
        )
        result = await self.session.execute(stmt)
        self.logger.info(
            f"Запрос на получение сообщений для conversation_id:{conversation_id}"
        )
        return [MessageMapper.to_domain(m) for m in result.scalars().all()]

    async def soft_delete(self, message_id: UUID) -> bool:
        message = await self.session.get(MessageORM, message_id)
        if message is None:
            self.logger.warning(f"Сообщение с ID:{message_id} не найдено.")
            return False
        message.is_deleted = True
        await self.session.flush()
        self.logger.info(
            f"Сообщение с ID:{message_id} помечено как удалённое в сессии."
        )
        return True

    async def delete(self, message_id: UUID) -> bool:
        message = await self.session.get(MessageORM, message_id)
        if message is None:
            self.logger.warning(f"Сообщение с ID:{message_id} не найдено.")
            return False
        await self.session.delete(message)
        await self.session.flush()
        self.logger.info(f"Сообщение с ID:{message_id} удалено из сессии.")
        return True
