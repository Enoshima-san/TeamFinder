from typing import Optional, cast
from uuid import UUID

from teamup.domain.entities import Message

from ..models.chat import MessageORM


class MessageMapper:
    @staticmethod
    def to_domain(orm: Optional[MessageORM]) -> Message:
        if orm is None:
            raise ValueError("ORM object is None")

        return Message(
            message_id=cast(UUID, orm.message_id),
            conversation_id=cast(UUID, orm.conversation_id),
            sender_id=cast(UUID, orm.sender_id),
            recipient_id=cast(UUID, orm.recipient_id),
            content=orm.content,
            created_at=orm.created_at,
            edited_at=orm.edited_at,
            is_deleted=orm.is_deleted,
            deleted_at=orm.deleted_at,
            is_read=orm.is_read,
            read_at=orm.read_at,
        )

    @staticmethod
    def to_orm(entity: Optional[Message]) -> MessageORM:
        if entity is None:
            raise ValueError("Entity is None")

        return MessageORM(
            message_id=entity.message_id,
            conversation_id=entity.conversation_id,
            sender_id=entity.sender_id,
            recipient_id=entity.recipient_id,
            content=entity.content,
            is_deleted=entity.is_deleted,
            created_at=entity.created_at,
            edited_at=entity.edited_at,
            deleted_at=entity.deleted_at,
            is_read=entity.is_read,
            read_at=entity.read_at,
        )
