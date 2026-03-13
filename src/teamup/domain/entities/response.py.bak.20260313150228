from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from ..enums import ResponseStatus
from .complaints import Complaints


@dataclass
class Response:
    announcement_id: UUID
    user_id: UUID
    response_id: UUID = field(default_factory=uuid4)
    status: str = ResponseStatus.PENDING.value
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    complaints: List["Complaints"] = field(default_factory=list)

    def set_status(self, status: str):
        """
        Назначить статус\n
        param:
            status - ResponseStatus.<PENDING/ACCEPTED/DECLINED>.value
        """
        self.status = status
        self.updated_at = datetime.now()

    @staticmethod
    def create(
        announcement_id: UUID,
        user_id: UUID,
        status: str = ResponseStatus.PENDING.value,
        created_at: datetime = datetime.now(),
        updated_at: datetime = datetime.now(),
    ):
        return Response(
            announcement_id=announcement_id,
            user_id=user_id,
            status=status,
            created_at=created_at,
            updated_at=updated_at,
        )
