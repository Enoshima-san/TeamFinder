from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from teamup.core import get_logger
from teamup.domain import INotificationRepository, Notification

from ...database.mappers import NotificationMapper
from ...database.models.chat import NotificationORM


class NotificationRepository(INotificationRepository):
    def __init__(self, session: AsyncSession):
        self.logger = get_logger()
        self.session = session
        self.logger.info("Инициализация NotificationRepository")

    async def create(self, notification: Notification) -> Optional[Notification]:
        try:
            orm = NotificationMapper.to_orm(notification)
            self.session.add(orm)
            await self.session.flush()
            await self.session.refresh(orm)
            self.logger.info(f"Создана уведомление: {orm.notification_id}")
            return NotificationMapper.to_domain(orm)
        except IntegrityError as e:
            self.logger.error(f"Ошибка при создании уведомления: {e}")
            return None

    async def get_by_id(self, notification_id: UUID) -> Optional[Notification]:
        notification = await self.session.get(NotificationORM, notification_id)
        if notification is None:
            self.logger.warning(f"Уведомление с ID:{notification_id} не найдено")
            return None
        return NotificationMapper.to_domain(notification)

    async def get_by_user_id(self, user_id: UUID) -> list[Notification]:
        stmt = select(NotificationORM).where(NotificationORM.notification_id == user_id)
        result = await self.session.execute(stmt)
        return [NotificationMapper.to_domain(n) for n in result.scalars().all()]

    async def get_by_conversation_id(self, conversation_id: UUID) -> list[Notification]:
        stmt = select(NotificationORM).where(
            NotificationORM.conversation_id == conversation_id
        )
        result = await self.session.execute(stmt)
        return [NotificationMapper.to_domain(n) for n in result.scalars().all()]

    async def get_by_announcement_id(self, announcement_id: UUID) -> list[Notification]:
        stmt = select(NotificationORM).where(
            NotificationORM.announcement_id == announcement_id
        )
        result = await self.session.execute(stmt)
        return [NotificationMapper.to_domain(n) for n in result.scalars().all()]

    async def delete(self, notification_id: UUID) -> bool:
        notification = await self.session.get(NotificationORM, notification_id)
        if notification is None:
            self.logger.warning(f"Уведомление с  ID:{notification_id} не найдено")
            return False
        await self.session.delete(notification)
        await self.session.flush()
        self.logger.info(f"Уведомление с ID:{notification_id} удалено")
        return True
