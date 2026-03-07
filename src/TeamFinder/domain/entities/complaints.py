from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from ..enums import ComplaintStatus


@dataclass
class Complaints:
    user_id: UUID
    announcement_id: UUID
    response_id: UUID
    complaint_id: UUID = field(default_factory=uuid4)

    status: str = ComplaintStatus.OPEN.value
    created_at: datetime = field(default_factory=datetime.now)
    resolved_at: Optional[datetime] = field(default_factory=datetime.now)

    def set_status(self, status: str):
        """Назначить статус\n
        param:
            status - ComplaintStatus.<OPEN/RESOLVED/DECLINED>.value
        """
        self.status = status

    def resolve(self):
        """Разрешить жалобу"""
        self.status = ComplaintStatus.RESOLVED.value
        self.resolved_at = datetime.now()

    @staticmethod
    def create(
        user_id: UUID,
        announcement_id: UUID,
        response_id: UUID,
        status: str = ComplaintStatus.OPEN.value,
        created_at: datetime = datetime.now(),
        resolved_at: datetime = datetime.now(),
    ) -> "Complaints":
        return Complaints(
            user_id=user_id,
            announcement_id=announcement_id,
            response_id=response_id,
            status=status,
            created_at=created_at,
            resolved_at=resolved_at,
        )
