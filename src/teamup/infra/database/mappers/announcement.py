from datetime import datetime
from typing import Any, cast
from uuid import UUID

from src.teamup.domain import Announcement

from ..models import AnnouncementORM
from ._map_relation import _map_relation
from .complaints import ComplaintsMapper
from .response import ResponseMapper


class AnnouncementMapper:
    @staticmethod
    def to_domain(orm: AnnouncementORM | None) -> Announcement:
        if not orm:
            raise ValueError("ORM object is None")

        complaints = _map_relation(orm, "complaints", ComplaintsMapper.to_domain)
        responses = _map_relation(orm, "response", ResponseMapper.to_domain)

        return Announcement(
            announcement_id=cast(UUID, orm.announcement_id),
            user_id=cast(UUID, orm.user_id),
            game_id=cast(UUID, orm.game_id),
            type=cast(Any, orm.type),
            rank_min=cast(None, orm.rank_min),
            rank_max=cast(None, orm.rank_max),
            description=cast(Any, orm.description),
            status=cast(Any, orm.status),
            created_at=cast(datetime, orm.created_at),
            updated_at=cast(datetime, orm.updated_at),
            response=responses,
            complaints=complaints,
        )

    @staticmethod
    def to_orm(entity: Announcement | None) -> AnnouncementORM:
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
