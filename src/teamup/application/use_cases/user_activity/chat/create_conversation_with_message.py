from uuid import UUID

from teamup.core import get_logger
from teamup.domain import (
    Conversation,
    IConversationRepository,
    Message,
)

from ....exceptions import ConversationCreationError
from .send_message import SendMessageUseCase


class CreateConversationWithMessageUseCase:
    def __init__(
        self,
        conv_r: IConversationRepository,
        sm_us: SendMessageUseCase,
    ):
        self.logger = get_logger()
        self._conv_r = conv_r
        self._sm_us = sm_us

    async def __call__(
        self,
        sender_id: UUID,
        recipient_id: UUID,
        announcement_id: UUID,
        message_content: str,
    ) -> tuple[Conversation, Message]:
        new_conversation = Conversation.create(
            announcement_author_id=recipient_id,
            responder_id=sender_id,
            announcement_id=announcement_id,
        )
        conversation = await self._conv_r.create(new_conversation)
        if conversation is None:
            raise ConversationCreationError("Не удалось создать диалог.")
        message = Message.create(
            conversation_id=conversation.conversation_id,
            sender_id=sender_id,
            recipient_id=recipient_id,
            content=message_content,
        )
        new_message = await self._sm_us(message)

        return new_conversation, new_message
