from src.teamup.domain import Announcement

from ..models import AnnouncementORM
from .complaints import ComplaintsMapper
from .response import ResponseMapper


class AnnouncementMapper:
    @staticmethod
    def to_domain(orm: AnnouncementORM | None) -> Announcement:
        if not orm:
            raise ValueError("ORM object is None")

        complaints = [ComplaintsMapper.to_domain(c) for c in orm.complaints]
        responses = [ResponseMapper.to_domain(r) for r in orm.responses]

        return Announcement(
            announcement_id=orm.announcement_id,  # type: ignore[reportArgumentType]
            user_id=orm.user_id,  # type: ignore[reportArgumentType]
            game_id=orm.game_id,  # type: ignore[reportArgumentType]
            type=orm.type,  # type: ignore[reportArgumentType]
            rank_min=orm.rank_min,  # type: ignore[reportArgumentType]
            rank_max=orm.rank_max,  # type: ignore[reportArgumentType]
            description=orm.description,  # type: ignore[reportArgumentType]
            status=orm.status,  # type: ignore[reportArgumentType]
            created_at=orm.created_at,  # type: ignore[reportArgumentType]
            updated_at=orm.updated_at,  # type: ignore[reportArgumentType]
            responses=responses,
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
