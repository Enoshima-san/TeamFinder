from uuid import UUID

from teamup.domain import (
    Announcement,
    Conversation,
    IAnnouncementRepository,
    IConversationRepository,
    IUserRepository,
)

from ....base_rules import BaseRules
from ....exceptions import ForbiddenError


class CheckConversationAccessUseCase:
    def __init__(
        self,
        user_id: UUID,
        ann_r: IAnnouncementRepository,
        user_r: IUserRepository,
        conv_r: IConversationRepository,
    ):
        self._user_id = user_id
        self._ann_r = ann_r
        self._user_r = user_r
        self._conv_r = conv_r

    async def __call__(
        self,
        conversation_id: UUID,
        announcement_id: UUID,
        user_id: UUID,
    ) -> tuple[Conversation, Announcement]:
        announcement = await BaseRules.get_announcement_or_fail(
            self._ann_r, announcement_id
        )
        conversation = await BaseRules.get_conversation_or_fail(
            self._conv_r, conversation_id
        )
        if announcement.user_id != conversation.announcement_author_id:
            raise ForbiddenError("Нет доступа к чату")
        if self._user_id != conversation.responder_id:
            raise ForbiddenError("...")

        return conversation, announcement
