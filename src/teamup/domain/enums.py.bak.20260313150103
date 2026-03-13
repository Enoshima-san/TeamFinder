from enum import Enum


class AnnouncementStatus(str, Enum):
    ACTIVE = "активный"
    PAUSED = "приостановлен"
    COMPLETED = "завершен"


class ResponseStatus(str, Enum):
    PENDING = "рассматривается"
    ACCEPTED = "принят"
    DECLINED = "отклонен"


class ComplaintStatus(str, Enum):
    OPEN = "открыт"
    RESOLVED = "решен"
    DECLINED = "отклонен"


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"


class PlayersBehavior(int, Enum):
    MIN_RATING = 1
    MAX_RATING = 100
    NEUTRAL = 50
