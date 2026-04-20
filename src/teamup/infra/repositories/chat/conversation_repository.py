from typing import Optional
from uuid import UUID

from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from teamup.domain import Conversation, IConversationRepository

from ...database.mappers import ConversationMapper
from ...database.models.chat import ConversationORM


class ConversationRepository(IConversationRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.logger.info("Инициализация ConversationRepository")

    async def create(self, conversation: Conversation) -> Optional[Conversation]:
        try:
            orm = ConversationMapper.to_orm(conversation)
            self.session.add(orm)
            await self.session.flush()
            await self.session.refresh(orm)
            self.logger.info("Диалог сохранен в сессии.")
            return ConversationMapper.to_domain(orm)
        except IntegrityError as e:
            self.logger.error(f"Ошибка при создании Conversation: {e}")
            return None

    async def get_by_id(self, conversation_id: UUID) -> Optional[Conversation]:
        conversation = await self.session.get(ConversationORM, conversation_id)
        if conversation is None:
            self.logger.warning(f"Диалог с ID:{conversation_id} не найден.")
            return None
        self.logger.info("Запрос на диалог с ID:{conversation_id}.")
        return ConversationMapper.to_domain(conversation)

    async def get_by_user_id(self, user_id: UUID) -> list[Conversation]:
        stmt = select(ConversationORM).where(
            or_(
                ConversationORM.announcement_author_id == user_id,
                ConversationORM.responder_id == user_id,
            )
        )
        result = await self.session.execute(stmt)
        self.logger.info(f"Запрос на диалоги для пользователя с ID:{user_id}.")
        return [ConversationMapper.to_domain(orm) for orm in result.scalars().all()]

    async def get_by_announcement_id(self, announcement_id: UUID) -> list[Conversation]:
        stmt = select(ConversationORM).where(
            ConversationORM.announcement_id == announcement_id
        )
        result = await self.session.execute(stmt)
        self.logger.info(f"Запрос на диалоги для объявления с ID:{announcement_id}.")
        return [ConversationMapper.to_domain(orm) for orm in result.scalars().all()]

    async def delete(self, conversation_id: UUID) -> bool:
        conversation = await self.session.get(ConversationORM, conversation_id)
        if conversation is None:
            self.logger.warning(f"Диалог с ID:{conversation_id} не найден.")
            return False
        await self.session.delete(conversation)
        await self.session.flush()
        self.logger.info(f"Диалог с ID:{conversation_id} удален из сессии.")
        return True
