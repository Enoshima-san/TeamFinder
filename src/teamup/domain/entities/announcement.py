from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from ..enums import AnnouncementStatus
from .complaints import Complaints
from .response import Response


@dataclass
class Announcement:
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

    response: List["Response"] = field(default_factory=list)
    complaints: List["Complaints"] = field(default_factory=list)

    def start(self):
        """Запуск ананонса"""
        if self.status == AnnouncementStatus.ACTIVE.value:
            raise ValueError("Анонс уже активен!")
        if self.status == AnnouncementStatus.PAUSED.value:
            raise ValueError("Анонс уже приостановлен!")
        if self.status == AnnouncementStatus.COMPLETED.value:
            raise ValueError("Анонс уже завершён!")
        self.status = AnnouncementStatus.ACTIVE.value
        self.updated_at = datetime.now()

    def pause(self):
        """Приостановка анонса"""
        if self.status == AnnouncementStatus.COMPLETED.value:
            raise ValueError("Невозможно приостановить завершённый анонс!")
        self.status = AnnouncementStatus.PAUSED.value
        self.updated_at = datetime.now()

    def complete(self):
        """Завершение анонса"""
        if self.status == AnnouncementStatus.COMPLETED.value:
            raise ValueError("Анонс уже завершён!")
        self.status = AnnouncementStatus.COMPLETED.value
        self.updated_at = datetime.now()

    def is_active(self) -> bool:
        """Проверка активности анонса"""
        return self.status == AnnouncementStatus.ACTIVE.value

    def set_description(self, description: str):
        """Смена описания анонсу"""
        if len(description) > 255:
            raise ValueError("Описание анонса должно быть не более 255 символов!")
        self.description = description
        self.updated_at = datetime.now()

    def set_ranks(self, rank_min: int, rank_max: int):
        """Смена требуемых раногов анонса"""
        if rank_min < 0 or rank_max < 0:
            raise ValueError("Ранги должны быть неотрицательными числами!")
        if rank_min > rank_max:
            raise ValueError("Минимальный ранг не может быть больше максимального!")

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

        if rank_min and rank_max:
            if rank_min < 0 or rank_max < 0:
                raise ValueError("Ранги должны быть неотрицательными числами!")
            if rank_min > rank_max:
                raise ValueError("Минимальный ранг не может быть больше максимального!")

        if description:
            if len(description) > 255:
                raise ValueError("Описание анонса должно быть не более 255 символов!")

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
