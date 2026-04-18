from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class Message:
    sender_id: UUID
    recipient_id: UUID
    conversation_id: UUID
    content: str
    created_at: datetime = field(default_factory=datetime.now)
    edited_at: Optional[datetime] = None
    is_deleted: bool = False
    deleted_at: Optional[datetime] = None
    is_read: bool = False
    read_at: Optional[datetime] = None

    message_id: UUID = field(default_factory=uuid4)

    def edit(self, _content: str):
        self.content = _content
        self.edited_at = datetime.now()

    def mark_as_read(self):
        self.is_read = True
        self.read_at = datetime.now()

    def delete(self):
        self.content = "Удалено"
        self.deleted_at = datetime.now()

    @staticmethod
    def create(
        sender_id: UUID,
        recipient_id: UUID,
        conversation_id: UUID,
        content: str,
    ) -> "Message":
        return Message(
            sender_id=sender_id,
            recipient_id=recipient_id,
            conversation_id=conversation_id,
            content=content,
        )
