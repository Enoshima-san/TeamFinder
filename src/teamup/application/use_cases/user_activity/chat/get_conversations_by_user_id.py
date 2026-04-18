from uuid import UUID

from teamup.domain import IConversationRepository, IUserRepository
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
        return [
            ConversationResponse(
                conversation_id=c.conversation_id, last_message_at=c.last_message_at
            )
            for c in conversations
        ]
