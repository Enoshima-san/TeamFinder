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
        ann_r: IAnnouncementRepository,
        user_r: IUserRepository,
        conv_r: IConversationRepository,
    ):
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
        is_author = user_id == conversation.announcement_author_id
        is_responder = user_id == conversation.responder_id
        if not (is_author or is_responder):
            raise ForbiddenError("Пользователь не является участником диалога")
        if announcement.announcement_id != conversation.announcement_id:
            raise ForbiddenError("Диалог не относится к этому объявлению")
        return conversation, announcement
