```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from ..enums import AnnouncementStatus
from .complaints import Complaints
from .response import Response


@dataclass
class Announcement:
    """
    Represents an announcement.

    Attributes:
        user_id (UUID): The ID of the user who created the announcement.
        game_id (UUID): The ID of the game associated with the announcement.
        announcement_id (UUID): The ID of the announcement.
        type (Optional[str]): The type of the announcement.
        rank_min (Optional[int]): The minimum rank required for the announcement.
        rank_max (Optional[int]): The maximum rank required for the announcement.
        description (Optional[str]): The description of the announcement.
        status (str): The status of the announcement.
        created_at (datetime): The date and time the announcement was created.
        updated_at (datetime): The date and time the announcement was last updated.
        responses (List[Response]): A list of responses to the announcement.
        complaints (List[Complaints]): A list of complaints about the announcement.
    """

    user_id: UUID
    game_id: UUID
    announcement_id: UUID = field(default_factory=uuid4)

    type: Optional[str] = None
    rank_min: Optional[int] = None
    rank_max: Optional[int] = None
    description: Optional[str] = None
    status: str = AnnouncementStatus.ACTIVE.value
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    responses: List["Response"] = field(default_factory=list)
    complaints: List["Complaints"] = field(default_factory=list)

    def start(self) -> None:
        """
        Starts the announcement.

        Raises:
            ValueError: If the announcement is already active, paused, or completed.
        """
        if self.status == AnnouncementStatus.ACTIVE.value:
            raise ValueError("Announcement is already active!")
        if self.status == AnnouncementStatus.PAUSED.value:
            raise ValueError("Announcement is already paused!")
        if self.status == AnnouncementStatus.COMPLETED.value:
            raise ValueError("Announcement is already completed!")
        self.status = AnnouncementStatus.ACTIVE.value
        self.updated_at = datetime.now()

    def pause(self) -> None:
        """
        Pauses the announcement.

        Raises:
            ValueError: If the announcement is already completed.
        """
        if self.status == AnnouncementStatus.COMPLETED.value:
            raise ValueError("Cannot pause a completed announcement!")
        self.status = AnnouncementStatus.PAUSED.value
        self.updated_at = datetime.now()

    def complete(self) -> None:
        """
        Completes the announcement.

        Raises:
            ValueError: If the announcement is already completed.
        """
        if self.status == AnnouncementStatus.COMPLETED.value:
            raise ValueError("Announcement is already completed!")
        self.status = AnnouncementStatus.COMPLETED.value
        self.updated_at = datetime.now()

    def is_active(self) -> bool:
        """
        Checks if the announcement is active.

        Returns:
            bool: True if the announcement is active, False otherwise.
        """
        return self.status == AnnouncementStatus.ACTIVE.value

    def set_description(self, description: str) -> None:
        """
        Sets the description of the announcement.

        Args:
            description (str): The new description of the announcement.

        Raises:
            ValueError: If the description is longer than 255 characters.
        """
        if len(description) > 255:
            raise ValueError("Description must be 255 characters or less!")
        self.description = description
        self.updated_at = datetime.now()

    def set_ranks(self, rank_min: int, rank_max: int) -> None:
        """
        Sets the ranks required for the announcement.

        Args:
            rank_min (int): The minimum rank required.
            rank_max (int): The maximum rank required.

        Raises:
            ValueError: If the ranks are invalid.
        """
        if rank_min < 0 or rank_max < 0:
            raise ValueError("Ranks must be non-negative!")
        if rank_min > rank_max:
            raise ValueError("Minimum rank cannot be greater than maximum rank!")

        self.rank_min = rank_min
        self.rank_max = rank_max
        self.updated_at = datetime.now()

    @staticmethod
    def create(
        user_id: UUID,
        game_id: UUID,
        type: Optional[str] = None,
        rank_min: Optional[int] = None,
        rank_max: Optional[int] = None,
        description: Optional[str] = None,
        status: str = AnnouncementStatus.ACTIVE.value,
        created_at: datetime = field(default_factory=datetime.now),
        updated_at: datetime = field(default_factory=datetime.now),
    ) -> "Announcement":
        """
        Creates a new announcement.

        Args:
            user_id (UUID): The ID of the user who created the announcement.
            game_id (UUID): The ID of the game associated with the announcement.
            type (Optional[str]): The type of the announcement.
            rank_min (Optional[int]): The minimum rank required for the announcement.
            rank_max (Optional[int]): The maximum rank required for the announcement.
            description (Optional[str]): The description of the announcement.
            status (str): The status of the announcement.
            created_at (datetime): The date and time the announcement was created.
            updated_at (datetime): The date and time the announcement was last updated.

        Returns:
            Announcement: The created announcement.
        """
        if rank_min and rank_max:
            if rank_min < 0 or rank_max < 0:
                raise ValueError("Ranks must be non-negative!")
            if rank_min > rank_max:
                raise ValueError("Minimum rank cannot be greater than maximum rank!")

        if description:
            if len(description) > 255:
                raise ValueError("Description must be 255 characters or less!")

        return Announcement(
            user_id=user_id,
            game_id=game_id,
            type=type,
            rank_min=rank_min,
            rank_max=rank_max,
            description=description,
            status=status,
            created_at=created_at,
            updated_at=updated_at,
        )
```