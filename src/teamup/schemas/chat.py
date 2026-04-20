from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from teamup.domain import Message


class ConversationWithMessages(BaseModel):
    conversation_id: UUID
    interlocutor: str
    messages: list[Message]


class ConversationResponse(BaseModel):
    conversation_id: UUID
    announcement_id: UUID
    interlocutor: str
    last_message_at: Optional[datetime]
