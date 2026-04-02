from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession

from teamup.application.check_rules import (
    check_ownership_or_admin,
    get_game_or_fail,
    get_user_or_fail,
)
from teamup.core import get_logger
from teamup.infra.database import get_async_session
from teamup.schemas import (
    AnnouncementCreateIn,
    AnnouncementOut,
    AnnouncementUpdateIn,
    GameBriefDto,
    TokenData,
    UserBriefDto,
)

from ..di import (
    get_announcement_listing_service,
    get_current_user,
    get_user_games_use_case,
)
from .responses import responses_router

logger = get_logger()


feed_router = APIRouter(tags=["Feed/Announcements"], prefix="/a")

feed_router.include_router(responses_router)


@feed_router.get("/", response_model=list[AnnouncementOut])
async def get_all_announcememnt(
    token_data: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    logger.info("Запрос на вывод всех активных объявлений.")
    ann_s = await get_announcement_listing_service(db)

    await get_user_or_fail(db, token_data.user_id)
    announcements = await ann_s.get_active_announcements(token_data.user_id)

    res = [
        AnnouncementOut(
            announcement_id=a.announcement_id,
            type=a.type,
            rank_max=a.rank_max,
            rank_min=a.rank_min,
            status=a.status,
            updated_at=a.updated_at,
            description=a.description,
            user=UserBriefDto.from_user(u),
            game=GameBriefDto.from_game(g),
        )
        for a, u, g in announcements
    ]
    return res


@feed_router.post("/new")
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

    ann_s = await get_announcement_listing_service(db)

    announcement = await ann_s.create_announcement(req, token_data.user_id)
    user = await get_user_or_fail(db, token_data.user_id)
    game = await get_game_or_fail(db, announcement.game_id)

    res = AnnouncementOut.create(announcement, user, game)
    logger.info(
        f"Объявление {announcement.announcement_id} успешно создано пользователем {user.user_id}."
    )

    await db.commit()
    return res


@feed_router.get("/{announcement_id}", response_model=AnnouncementOut)
async def get_announcement(
    announcement_id: UUID,
    token_data: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    ann_s = await get_announcement_listing_service(db)
    await get_user_or_fail(db, token_data.user_id)
    announcement, user, game = await ann_s.get_announcement_by_id(
        announcement_id, token_data.user_id
    )
    res = AnnouncementOut.create(announcement, user, game)
    return res


@feed_router.delete("/{announcement_id}")
async def delete_announcement(
    announcement_id: UUID,
    token_data: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    ann_s = await get_announcement_listing_service(db)

    await check_ownership_or_admin(db, announcement_id, token_data.user_id)

    await ann_s.delete_announcement(announcement_id, token_data.user_id)
    await db.commit()
    return Response(status_code=204)


@feed_router.patch("/{announcement_id}", response_model=AnnouncementOut)
async def update_announcement(
    announcement_id: UUID,
    req: AnnouncementUpdateIn,
    token_data: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    ann_s = await get_announcement_listing_service(db)

    await check_ownership_or_admin(db, token_data.user_id, announcement_id)

    ann, user, game = await ann_s.update_announcement(req, token_data.user_id)
    res = AnnouncementOut.create(ann, user, game)
    await db.commit()
    return res
