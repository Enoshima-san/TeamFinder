from uuid import UUID

from teamup.domain import (
    IConversationRepository,
    IUserRepository,
)
from teamup.domain.repositories import IMessageRepository
from teamup.schemas import ConversationWithMessages

from ....base_rules import BaseRules
from ....exceptions import ForbiddenError, UserNotFoundError


class GetConversationWithMessagesUseCase:
    def __init__(
        self,
        mess_r: IMessageRepository,
        user_r: IUserRepository,
        conv_r: IConversationRepository,
    ):
        self._mess_r = mess_r
        self._user_r = user_r
        self._conv_r = conv_r

    async def __call__(
        self,
        conversation_id: UUID,
        user_id: UUID,
    ) -> ConversationWithMessages:
        user = await BaseRules.get_user_or_fail(self._user_r, user_id)
        conversation = await BaseRules.get_conversation_or_fail(
            self._conv_r, conversation_id
        )
        if not conversation.is_participant(user.user_id):
            raise ForbiddenError("Пользователь не является участником чата")

        interlocutor = None
        if user.user_id == conversation.announcement_author_id:
            interlocutor = await self._user_r.get_by_id(conversation.responder_id)
        else:
            interlocutor = await self._user_r.get_by_id(
                conversation.announcement_author_id
            )

        if interlocutor is None:
            raise UserNotFoundError("Пользователь не найден")

        messages_list = await self._mess_r.get_by_conversation_id(
            conversation.conversation_id
        )
        return ConversationWithMessages(
            conversation_id=conversation.conversation_id,
            interlocutor=interlocutor.username,
            messages=messages_list,
        )
