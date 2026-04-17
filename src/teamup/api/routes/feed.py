from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from teamup.application.check_rules import (
    check_ownership_or_admin,
    get_game_or_fail,
    get_user_or_fail,
)
from teamup.application.di import (
    get_announcement_service,
    get_user_games_use_case,
)
from teamup.core import get_logger
from teamup.core.di import get_current_user
from teamup.infra.database import get_async_session
from teamup.schemas import (
    AnnouncementCreateIn,
    AnnouncementSummaryOut,
    AnnouncementUpdateIn,
    TokenData,
)

from .responses import responses_router

logger = get_logger()


feed_router = APIRouter(tags=["Feed/Announcements"], prefix="/a")

feed_router.include_router(responses_router)


@feed_router.get("/", response_model=list[AnnouncementSummaryOut])
async def get_all_announcememnt(
    db: AsyncSession = Depends(get_async_session),
):
    logger.info("Запрос на вывод всех активных объявлений.")
    ann_s = await get_announcement_service(db)

    res = await ann_s.get_active_announcements()

    return res


@feed_router.post(
    "/new", response_model=AnnouncementSummaryOut, status_code=status.HTTP_201_CREATED
)
async def create_announcement(
    req: AnnouncementCreateIn,
    token_data: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    ug_uc = await get_user_games_use_case(db)
    user_games = await ug_uc(token_data.user_id)
    if len(user_games) == 0:
        raise HTTPException(status_code=400, detail="У пользовтеля нет игр.")
    if not any(game.game_id == req.game_id for game in user_games):
        raise HTTPException(
            status_code=400,
            detail="Пользователь не может создать объявление с игрой, которой нет в его библиотеке.",
        )

    ann_s = await get_announcement_service(db)

    user = await get_user_or_fail(db, token_data.user_id)
    game = await get_game_or_fail(db, req.game_id)
    announcement = await ann_s.create_announcement(req, token_data.user_id)

    res = AnnouncementSummaryOut.create(announcement, user, game)
    logger.info(
        f"Объявление {announcement.announcement_id} успешно создано пользователем {user.user_id}."
    )

    await db.commit()
    return res


@feed_router.get("/{announcement_id}", response_model=AnnouncementSummaryOut)
async def get_announcement(
    announcement_id: UUID,
    token_data: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    ann_s = await get_announcement_service(db)
    await get_user_or_fail(db, token_data.user_id)
    res = await ann_s.get_announcement_by_id(announcement_id)
    return res


@feed_router.delete("/{announcement_id}")
async def delete_announcement(
    announcement_id: UUID,
    token_data: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    ann_s = await get_announcement_service(db)

    await check_ownership_or_admin(db, announcement_id, token_data.user_id)

    await ann_s.delete_announcement(announcement_id, token_data.user_id)
    await db.commit()
    return Response(status_code=204)


@feed_router.patch("/{announcement_id}", response_model=AnnouncementSummaryOut)
async def update_announcement(
    announcement_id: UUID,
    req: AnnouncementUpdateIn,
    token_data: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    ann_s = await get_announcement_service(db)

    await check_ownership_or_admin(db, token_data.user_id, announcement_id)

    res = await ann_s.update_announcement(req, token_data.user_id)
    await db.commit()
    return res
