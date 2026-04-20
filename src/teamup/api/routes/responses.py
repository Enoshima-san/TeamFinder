from uuid import UUID

from fastapi import APIRouter, Depends, status

from teamup.application.di import (
    get_announcement_service,
    get_create_conversation_use_case,
    get_responses_service,
)
from teamup.application.services import AnnouncementService, ResponsesService
from teamup.application.use_cases import CreateConversationWithMessageUseCase
from teamup.core.di import get_current_user
from teamup.schemas import (
    ResponseCreationIn,
    ResponseCreationOut,
    ResponseOut,
    TokenData,
)

responses_router = APIRouter(tags=["Feed/Responses"])


@responses_router.post(
    "/{announcement_id}/responses/new",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseCreationOut,
)
async def create_response(
    req: ResponseCreationIn,
    announcement_id: UUID,
    res_s: ResponsesService = Depends(get_responses_service),
    ann_s: AnnouncementService = Depends(get_announcement_service),
    cm_us: CreateConversationWithMessageUseCase = Depends(
        get_create_conversation_use_case
    ),
    token_data: TokenData = Depends(get_current_user),
):
    response = await res_s.create_response(announcement_id, token_data.user_id)
    announcement = await ann_s.get_announcement_by_id(announcement_id)
    conversation, message = await cm_us(
        sender_id=token_data.user_id,
        recipient_id=announcement.user_id,
        announcement_id=announcement_id,
        message_content=req.message,
    )
    res = ResponseCreationOut.create(response, conversation, message)
    return res


@responses_router.get("/{announcement_id}/responses/", response_model=list[ResponseOut])
async def get_responses_by_announcement(
    announcement_id: UUID,
    res_s: ResponsesService = Depends(get_responses_service),
    token_data: TokenData = Depends(get_current_user),
):
    res = await res_s.get_responses_by_announcement(announcement_id)
    return [
        ResponseOut(
            user_id=r.user_id,
            announcement_id=r.announcement_id,
            status=r.status,
            created_at=r.created_at,
            updated_at=r.updated_at,
        )
        for r in res
    ]
