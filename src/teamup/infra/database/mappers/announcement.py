from typing import Optional, cast
from uuid import UUID

from teamup.domain import Announcement

from ..models import AnnouncementORM
from ._map_relation import _map_relation
from .complaints import ComplaintsMapper
from .conversation import ConversationMapper
from .notification import NotificationMapper
from .response import ResponseMapper


class AnnouncementMapper:
    @staticmethod
    def to_domain(orm: Optional[AnnouncementORM]) -> Announcement:
        if orm is None:
            raise ValueError("ORM object is None")

        complaints = _map_relation(orm, "complaints", ComplaintsMapper.to_domain)
        responses = _map_relation(orm, "response", ResponseMapper.to_domain)
        conversations = _map_relation(orm, "conversation", ConversationMapper.to_domain)
        notifications = _map_relation(orm, "notification", NotificationMapper.to_domain)

        return Announcement(
            announcement_id=cast(UUID, orm.announcement_id),
            user_id=cast(UUID, orm.user_id),
            game_id=cast(UUID, orm.game_id),
            type=orm.type,
            rank_min=orm.rank_min,
            rank_max=orm.rank_max,
            description=orm.description,
            status=orm.status,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
            announcement_responses=responses,
            announcement_complaints=complaints,
            announcement_conversations=conversations,
            announcement_notifications=notifications,
        )

    @staticmethod
    def to_orm(entity: Optional[Announcement]) -> AnnouncementORM:
        if not entity:
            raise ValueError("Entity is None")

        return AnnouncementORM(
            announcement_id=entity.announcement_id,
            user_id=entity.user_id,
            game_id=entity.game_id,
            type=entity.type,
            rank_min=entity.rank_min,
            rank_max=entity.rank_max,
            description=entity.description,
            status=entity.status,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
