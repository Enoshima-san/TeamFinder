from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class Notification:
    user_id: UUID
    announcement_id: UUID
    conversation_id: UUID
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    is_read: bool = False

    notification_id: UUID = field(default_factory=uuid4)

    def mark_as_read(self):
        self.is_read = True

    def set_content(self, _content: str):
        self.content = _content
