from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from teamup.infra.database import get_async_session
from teamup.schemas import ResponseOut, TokenData

from ..di import get_current_user, get_responses_service

responses_router = APIRouter(tags=["Feed/Responses"])


@responses_router.post(
    "/{announcement_id}/responses/new",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseOut,
)
async def create_response(
    announcement_id: UUID,
    token_data: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    res_s = await get_responses_service(db)
    res = await res_s.create_response(announcement_id, token_data.user_id)

    await db.commit()
    return ResponseOut(
        user_id=res.user_id,
        announcement_id=res.announcement_id,
        status=res.status,
        created_at=res.created_at,
        updated_at=res.updated_at,
    )


@responses_router.get("/{announcement_id}/responses/", response_model=list[ResponseOut])
async def get_responses_by_announcement(
    announcement_id: UUID,
    token_data: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
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
