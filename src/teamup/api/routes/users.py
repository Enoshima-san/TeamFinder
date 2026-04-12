from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from teamup.infra.database import get_async_session
from teamup.schemas import (
    AnnouncementBriefDto,
    FullUserInfoResponse,
    GameBriefDto,
    ResponseBriefDto,
    TokenData,
    UserResponse,
)

from ..di import (
    get_current_user,
    get_full_user_info_use_case,
    get_user_games_use_case,
    get_user_use_case,
)

user_router = APIRouter(tags=["Users"], prefix="/users")


@user_router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    token_data: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    """
    Берет информацию из JWT и сверяет с БД
    """
    usecase = await get_user_use_case(db)
    user = await usecase(token_data.user_id)
    return UserResponse(
        user_id=user.user_id,
        username=user.username,
        email=user.email,
        registration_date=user.registration_date,
        age=user.age,
        about_me=user.about_me,
    )


@user_router.get("/{user_id}", response_model=FullUserInfoResponse)
async def get_full_user_info(
    user_id: UUID,
    db: AsyncSession = Depends(get_async_session),
):
    """
    Возвращает полную информацию о пользователе
    """
    u_usecase = await get_full_user_info_use_case(db)
    user = await u_usecase(user_id)

    g_usercase = await get_user_games_use_case(db)
    games = await g_usercase(user_id)
    return FullUserInfoResponse(
        user_id=user.user_id,
        username=user.username,
        email=user.email,
        registration_date=user.registration_date,
        last_login=user.last_login,
        is_active=user.is_active,
        role=user.role,
        has_microphone=user.has_microphone,
        age=user.age,
        about_me=user.about_me,
        is_blocked=user.is_blocked,
        blocked_reason=user.blocked_reason,
        games=[GameBriefDto.from_game(g) for g in games],
        announcements=[
            AnnouncementBriefDto.from_announcement(a) for a in user.user_announcement
        ],
        responses=[ResponseBriefDto.from_response(r) for r in user.user_response],
    )
