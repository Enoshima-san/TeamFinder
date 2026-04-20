from typing import Optional, cast
from uuid import UUID

from teamup.domain import Response

from ..models import ResponseORM
from ._map_relation import _map_relation
from .complaints import ComplaintsMapper


class ResponseMapper:
    @staticmethod
    def to_domain(orm: Optional[ResponseORM]) -> Response:
        if not orm:
            raise ValueError("ORM object is None")

        complaints = _map_relation(orm, "complaints", ComplaintsMapper.to_domain)

        return Response(
            response_id=cast(UUID, orm.response_id),
            announcement_id=cast(UUID, orm.announcement_id),
            user_id=cast(UUID, orm.user_id),
            status=orm.status,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
            response_complaints=complaints,
        )

    @staticmethod
    def to_orm(entity: Optional[Response]) -> ResponseORM:
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
