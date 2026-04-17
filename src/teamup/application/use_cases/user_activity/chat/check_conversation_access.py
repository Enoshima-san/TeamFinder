# teamup/application/chat/check_conversation_access.py
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from teamup.application.check_rules import (
    get_announcement_or_fail,
    get_conversation_or_fail,
)
from teamup.domain import Announcement, Conversation

from ....exceptions import ForbiddenError


class CheckConversationAccessUseCase:
    def __init__(self, db: AsyncSession, user_id: UUID):
        self._db = db
        self._user_id = user_id

    async def __call__(
        self,
        conversation_id: UUID,
        announcement_id: UUID,
        user_id: UUID,
    ) -> tuple[Conversation, Announcement]:
        announcement = await get_announcement_or_fail(self._db, announcement_id)
        conversation = await get_conversation_or_fail(self._db, conversation_id)
        if announcement.user_id != conversation.announcement_author_id:
            raise ForbiddenError("Нет доступа к чату")
        if self._user_id != conversation.responder_id:
            raise ForbiddenError("...")

        return conversation, announcement
