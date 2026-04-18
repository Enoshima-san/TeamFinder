from typing import Optional, cast
from uuid import UUID

from teamup.domain import Conversation

from ..models.chat import ConversationORM
from ._map_relation import _map_relation
from .message import MessageMapper
from .notification import NotificationMapper


class ConversationMapper:
    @staticmethod
    def to_domain(orm: Optional[ConversationORM]) -> Conversation:
        if orm is None:
            raise ValueError("Entity is None")

        conversation_messages = _map_relation(orm, "message", MessageMapper.to_domain)
        conversation_notifications = _map_relation(
            orm, "notification", NotificationMapper.to_domain
        )

        return Conversation(
            conversation_id=cast(UUID, orm.conversation_id),
            announcement_id=cast(UUID, orm.announcement_id),
            announcement_author_id=cast(UUID, orm.announcement_author_id),
            responder_id=cast(UUID, orm.responder_id),
            created_at=orm.created_at,
            updated_at=orm.updated_at,
            last_message_at=orm.last_message_at,
            conversation_messages=conversation_messages,
            conversation_notifications=conversation_notifications,
        )

    @staticmethod
    def to_orm(entity: Optional[Conversation]) -> ConversationORM:
        if entity is None:
            raise ValueError("Entity is None")

        return ConversationORM(
            conversation_id=entity.conversation_id,
            announcement_id=entity.announcement_id,
            announcement_author_id=entity.announcement_author_id,
            responder_id=entity.responder_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            last_message_at=entity.last_message_at,
        )
