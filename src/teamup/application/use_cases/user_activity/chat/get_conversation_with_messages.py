from teamup.domain import Announcement, Conversation, User
from teamup.domain.repositories import IMessageRepository
from teamup.schemas import ConversationWithMessages

from ....exceptions import ConversationBadRequestError, ForbiddenError


class GetConversationWithMessagesUseCase:
    def __init__(self, m_r: IMessageRepository):
        self.m_r = m_r

    async def __call__(
        self, conversation: Conversation, user: User, announcement: Announcement
    ) -> ConversationWithMessages:
        if not conversation.is_participant(
            user.user_id
        ) or not conversation.is_participant(announcement.user_id):
            raise ForbiddenError("Пользователь не является участником чата")

        if user.user_id == announcement.user_id:
            raise ConversationBadRequestError(
                "Пользователь не может просматривать чат с самим собой"
            )

        messages_list = await self.m_r.get_by_conversation_id(
            conversation.conversation_id
        )
        return ConversationWithMessages(
            conversation_id=conversation.conversation_id, messages=messages_list
        )
