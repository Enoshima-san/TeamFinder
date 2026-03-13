from src.teamup.domain import Response

from ..models import ResponseORM
from .complaints import ComplaintsMapper


class ResponseMapper:
    @staticmethod
    def to_domain(orm: ResponseORM | None):
        if not orm:
            raise ValueError("ORM object is None")

        complaints = [ComplaintsMapper.to_domain(c) for c in orm.complaints]

        return Response(
            response_id=orm.response_id,  # type: ignore[reportArgumentType]
            announcement_id=orm.announcement_id,  # type: ignore[reportArgumentType]
            user_id=orm.user_id,  # type: ignore[reportArgumentType]
            status=orm.status,  # type: ignore[reportArgumentType]
            created_at=orm.created_at,  # type: ignore[reportArgumentType]
            updated_at=orm.updated_at,  # type: ignore[reportArgumentType]
            complaints=complaints,
        )

    @staticmethod
    def to_orm(entity: Response | None) -> ResponseORM:
        if not entity:
            raise ValueError("Entity is None")

        return ResponseORM(
            response_id=entity.response_id,
            announcement_id=entity.announcement_id,
            user_id=entity.user_id,
            status=entity.status,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
