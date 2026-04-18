from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from .message import Message
from .notification import Notification


@dataclass
class Conversation:
    announcement_id: UUID
    announcement_author_id: UUID
    responder_id: UUID
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    last_message_at: Optional[datetime] = None

    conversation_id: UUID = field(default_factory=uuid4)

    conversation_messages: list["Message"] = field(default_factory=list)
    conversation_notifications: list["Notification"] = field(default_factory=list)

    def is_participant(self, user_id: UUID) -> bool:
        return user_id in [self.announcement_author_id, self.responder_id]

    def update_last_message(self):
        self.last_message_at = datetime.now()
        self.updated_at = datetime.now()

    @staticmethod
    def create(
        announcement_id: UUID,
        announcement_author_id: UUID,
        responder_id: UUID,
    ) -> "Conversation":
        return Conversation(
            announcement_id=announcement_id,
            announcement_author_id=announcement_author_id,
            responder_id=responder_id,
        )

    def get_other_participant(self, user_id: UUID) -> UUID:
        """Возвращает второго участника диалога."""
        if user_id == self.responder_id:
            return self.announcement_author_id
        if user_id == self.announcement_author_id:
            return self.responder_id
        raise ValueError(f"User {user_id} is not a participant")
