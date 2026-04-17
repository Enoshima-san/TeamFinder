from typing import Optional, cast
from uuid import UUID

from teamup.domain import Notification

from ..models.chat import NotificationORM


class NotificationMapper:
    @staticmethod
    def to_domain(orm: Optional[NotificationORM]) -> Notification:
        if orm is None:
            raise ValueError("ORM object is None")

        return Notification(
            notification_id=cast(UUID, orm.notification_id),
            user_id=cast(UUID, orm.user_id),
            announcement_id=cast(UUID, orm.announcement_id),
            conversation_id=cast(UUID, orm.conversation_id),
            content=orm.content,
            timestamp=orm.timestamp,
            is_read=orm.is_read,
        )

    @staticmethod
    def to_orm(entity: Optional[Notification]) -> NotificationORM:
        if entity is None:
            raise ValueError("Entity is None")

        return NotificationORM(
            notification_id=entity.notification_id,
            user_id=entity.user_id,
            announcement_id=entity.announcement_id,
            conversation_id=entity.conversation_id,
            content=entity.content,
            timestamp=entity.timestamp,
            is_read=entity.is_read,
        )
