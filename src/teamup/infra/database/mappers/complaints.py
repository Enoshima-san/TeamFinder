from datetime import datetime
from typing import cast
from uuid import UUID

from src.teamup.domain import Complaints

from ..models import ComplaintsORM


class ComplaintsMapper:
    @staticmethod
    def to_domain(orm: ComplaintsORM | None) -> Complaints:
        if not orm:
            raise ValueError("ORM object is None")

        return Complaints(
            complaint_id=cast(UUID, orm.complaint_id),
            user_id=cast(UUID, orm.user_id),
            announcement_id=cast(UUID, orm.announcement_id),
            response_id=cast(UUID, orm.response_id),
            status=cast(str, orm.status),
            created_at=cast(datetime, orm.created_at),
            resolved_at=cast(datetime, orm.resolved_at),
        )

    @staticmethod
    def to_orm(entity: Complaints | None) -> ComplaintsORM:
        if not entity:
            raise ValueError("Entity is None")

        return ComplaintsORM(
            complaint_id=entity.complaint_id,
            user_id=entity.user_id,
            announcement_id=entity.announcement_id,
            response_id=entity.response_id,
            status=entity.status,
            created_at=entity.created_at,
            resolved_at=entity.resolved_at,
        )
