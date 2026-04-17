from uuid import UUID

from pydantic import BaseModel

from teamup.domain import Message


class ConversationWithMessages(BaseModel):
    conversation_id: UUID
    messages: list[Message]
