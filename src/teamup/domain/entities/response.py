```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from ..enums import ResponseStatus
from .complaints import Complaints


@dataclass
class Response:
    """
    Represents a response to an announcement.

    Attributes:
        announcement_id (UUID): Unique identifier of the announcement.
        user_id (UUID): Unique identifier of the user.
        response_id (UUID): Unique identifier of the response (auto-generated).
        status (str): Status of the response (e.g., PENDING, ACCEPTED, DECLINED).
        created_at (datetime): Timestamp when the response was created.
        updated_at (datetime): Timestamp when the response was last updated.
        complaints (List[Complaints]): List of complaints related to this response.
    """

    announcement_id: UUID
    user_id: UUID
    response_id: UUID = field(default_factory=uuid4)
    status: str = ResponseStatus.PENDING.value
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    complaints: List["Complaints"] = field(default_factory=list)

    def set_status(self, status: ResponseStatus) -> None:
        """
        Sets the status of the response.

        Args:
            status (ResponseStatus): New status of the response (e.g., PENDING, ACCEPTED, DECLINED).
        """
        self.status = status.value
        self.updated_at = datetime.now()

    @staticmethod
    def create(
        announcement_id: UUID,
        user_id: UUID,
        status: ResponseStatus = ResponseStatus.PENDING,
        created_at: datetime = datetime.now(),
        updated_at: datetime = datetime.now(),
    ) -> "Response":
        """
        Creates a new response instance.

        Args:
            announcement_id (UUID): Unique identifier of the announcement.
            user_id (UUID): Unique identifier of the user.
            status (ResponseStatus, optional): Status of the response (default: PENDING).
            created_at (datetime, optional): Timestamp when the response was created (default: now).
            updated_at (datetime, optional): Timestamp when the response was last updated (default: now).

        Returns:
            Response: New response instance.
        """
        return Response(
            announcement_id=announcement_id,
            user_id=user_id,
            status=status.value,
            created_at=created_at,
            updated_at=updated_at,
        )
```