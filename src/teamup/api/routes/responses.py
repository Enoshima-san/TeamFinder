from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from teamup.application.check_rules import get_announcement_or_fail, get_user_or_fail
from teamup.application.di import (
    get_create_conversation_use_case,
    get_responses_service,
)
from teamup.core.di import get_current_user
from teamup.infra.database import get_async_session
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
    token_data: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    res_s = await get_responses_service(db)
    cm_us = await get_create_conversation_use_case(db)

    user = await get_user_or_fail(db, token_data.user_id)
    announcement = await get_announcement_or_fail(db, announcement_id)
    response = await res_s.create_response(announcement_id, user.user_id)
    conversation, message = await cm_us(
        user.user_id, announcement.user_id, announcement_id, req.message
    )
    res = ResponseCreationOut.create(response, conversation, message)
    await db.commit()
    return res


@responses_router.get("/{announcement_id}/responses/", response_model=list[ResponseOut])
async def get_responses_by_announcement(
    announcement_id: UUID,
    token_data: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    await get_user_or_fail(db, token_data.user_id)
    await get_announcement_or_fail(db, announcement_id)
    res_s = await get_responses_service(db)
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
