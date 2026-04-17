from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from teamup.application.check_rules import (
    get_announcement_or_fail,
    get_conversation_or_fail,
    get_user_or_fail,
)
from teamup.application.di import get_conversation_with_messages_use_case
from teamup.core.di import get_current_user
from teamup.infra.database import get_async_session
from teamup.schemas import ConversationWithMessages, TokenData

chat_roter = APIRouter(tags=["chat"])


@chat_roter.post(
    "/a/{announcement_id}/{conversation_id}", response_model=ConversationWithMessages
)
async def open_chat(
    announcement_id: UUID,
    conversation_id: UUID,
    token_data: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    user = await get_user_or_fail(db, token_data.user_id)
    announcement = await get_announcement_or_fail(db, announcement_id)
    conversation = await get_conversation_or_fail(db, conversation_id)

    cwm_us = await get_conversation_with_messages_use_case(db)
    conversation_with_messages = await cwm_us(conversation, user, announcement)
    return conversation_with_messages
