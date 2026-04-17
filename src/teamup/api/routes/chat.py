from uuid import UUID

from fastapi import APIRouter, Depends

from teamup.application.di import (
    get_conversation_by_user_id_use_case,
    get_conversation_with_messages_use_case,
)
from teamup.application.use_cases import (
    GetConversationsByUserIdUseCase,
    GetConversationWithMessagesUseCase,
)
from teamup.core.di import get_current_user
from teamup.schemas import ConversationResponse, ConversationWithMessages, TokenData

chat_router = APIRouter(tags=["Chat"])


@chat_router.get("/chats/{conversation_id}", response_model=ConversationWithMessages)
async def open_chat(
    conversation_id: UUID,
    cwm_us: GetConversationWithMessagesUseCase = Depends(
        get_conversation_with_messages_use_case
    ),
    token_data: TokenData = Depends(get_current_user),
):
    conversation_with_messages = await cwm_us(
        user_id=token_data.user_id,
        conversation_id=conversation_id,
    )
    return conversation_with_messages


@chat_router.get("/chats", response_model=list[ConversationResponse])
async def get_conversations_by_user_id(
    cwm_us: GetConversationsByUserIdUseCase = Depends(
        get_conversation_by_user_id_use_case
    ),
    token_data: TokenData = Depends(get_current_user),
):
    res = await cwm_us(
        user_id=token_data.user_id,
    )
    return res
