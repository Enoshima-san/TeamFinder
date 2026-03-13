```python
from enum import Enum

# Enum class for announcement status
class AnnouncementStatus(str, Enum):
    """Enum class for announcement status."""
    ACTIVE = "активный"  # Announcement is active
    PAUSED = "приостановлен"  # Announcement is paused
    COMPLETED = "завершен"  # Announcement is completed


# Enum class for response status
class ResponseStatus(str, Enum):
    """Enum class for response status."""
    PENDING = "рассматривается"  # Response is pending
    ACCEPTED = "принят"  # Response is accepted
    DECLINED = "отклонен"  # Response is declined


# Enum class for complaint status
class ComplaintStatus(str, Enum):
    """Enum class for complaint status."""
    OPEN = "открыт"  # Complaint is open
    RESOLVED = "решен"  # Complaint is resolved
    DECLINED = "отклонен"  # Complaint is declined


# Enum class for user roles
class UserRole(str, Enum):
    """Enum class for user roles."""
    ADMIN = "admin"  # Admin user role
    USER = "user"  # User user role


# Enum class for player behavior
class PlayersBehavior(int, Enum):
    """Enum class for player behavior."""
    MIN_RATING = 1  # Minimum rating
    MAX_RATING = 100  # Maximum rating
    NEUTRAL = 50  # Neutral rating
```

```python
# Example usage
if __name__ == "__main__":
    # Get announcement status
    announcement_status = AnnouncementStatus.ACTIVE
    print(f"Announcement status: {announcement_status.value}")

    # Get response status
    response_status = ResponseStatus.ACCEPTED
    print(f"Response status: {response_status.value}")

    # Get complaint status
    complaint_status = ComplaintStatus.RESOLVED
    print(f"Complaint status: {complaint_status.value}")

    # Get user role
    user_role = UserRole.ADMIN
    print(f"User role: {user_role.value}")

    # Get player behavior
    player_behavior = PlayersBehavior.NEUTRAL
    print(f"Player behavior: {player_behavior.value}")
```