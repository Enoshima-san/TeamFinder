from uuid import UUID

from teamup.domain import Conversation, IConversationRepository, IUserRepository
from teamup.schemas import ConversationResponse

from ....base_rules import BaseRules


class GetConversationsByUserIdUseCase:
    def __init__(
        self,
        conv_r: IConversationRepository,
        user_r: IUserRepository,
    ):
        self._conv_r = conv_r
        self._user_r = user_r

    async def __call__(
        self,
        user_id: UUID,
    ) -> list[ConversationResponse]:
        await BaseRules.get_user_or_fail(self._user_r, user_id)
        conversations = await self._conv_r.get_by_user_id(user_id)
        interlocutor_usernames = await self._get_interlocutor(conversations, user_id)
        return [
            ConversationResponse(
                conversation_id=c.conversation_id,
                announcement_id=c.announcement_id,
                interlocutor=username,
                last_message_at=c.last_message_at,
            )
            for c, username in zip(conversations, interlocutor_usernames)
        ]

    async def _get_interlocutor(
        self, conversations: list[Conversation], user_id: UUID
    ) -> list[str]:
        res = []
        for c in conversations:
            if user_id == c.announcement_author_id:
                user = await BaseRules.get_user_or_fail(self._user_r, c.responder_id)
                res.append(user.username)
            else:
                user = await BaseRules.get_user_or_fail(
                    self._user_r, c.announcement_author_id
                )
                res.append(user.username)
        return res
