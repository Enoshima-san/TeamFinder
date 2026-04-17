from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from teamup.domain import Message


class ConversationWithMessages(BaseModel):
    conversation_id: UUID
    messages: list[Message]


class ConversationResponse(BaseModel):
    conversation_id: UUID
    last_message_at: Optional[datetime]
