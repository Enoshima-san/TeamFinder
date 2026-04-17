from uuid import UUID

from teamup.domain.repositories import IMessageRepository
from teamup.schemas import ConversationWithMessages


class GetConversationWithMessagesUseCase:
    def __init__(self, m_r: IMessageRepository):
        self.m_r = m_r

    async def __call__(self, conversation_id: UUID) -> ConversationWithMessages:
        messages_list = await self.m_r.get_by_conversation_id(conversation_id)
        return ConversationWithMessages(
            conversation_id=conversation_id, messages=messages_list
        )
