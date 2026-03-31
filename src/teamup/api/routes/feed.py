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
    get_responses_service,
    get_user_games_use_case,
)
from .responses import responses_router

from src.teamup.application import AnnouncementListingService
from src.teamup.core import get_logger
from src.teamup.schemas import AnnouncementCreateIn, AnnouncementUpdateIn, TokenData

from ..di import get_announcement_listing_service, get_current_user

feed_router = APIRouter(tags=["Feed"], prefix="/a")

logger = get_logger()


@feed_router.get("/")
async def get_all_announcememnt(
    announcement_service: AnnouncementListingService = Depends(
        get_announcement_listing_service
    ),
    user: TokenData = Depends(get_current_user),
):
    logger.info("Запрос на вывод всех активных объявлений.")
    announcements = await announcement_service.get_active_announcements(user.user_id)
    return announcements


@feed_router.post("/new")
async def create_announcement(
    req: AnnouncementCreateIn,
    announcement_service: AnnouncementListingService = Depends(
        get_announcement_listing_service
    ),
    user: TokenData = Depends(get_current_user),
):
    announcement = await announcement_service.create_announcement(req, user.user_id)

    return announcement


@feed_router.get("/{announcement_id}")
async def get_announcement(
    announcement_id: UUID,
    announcement_service: AnnouncementListingService = Depends(
        get_announcement_listing_service
    ),
    user: TokenData = Depends(get_current_user),
):
    announcement = await announcement_service.get_announcement_by_id(
        announcement_id, user.user_id
    )
    return announcement


@feed_router.delete("/{announcement_id}")
async def delete_announcement(
    announcement_id: UUID,
    announcement_service: AnnouncementListingService = Depends(
        get_announcement_listing_service
    ),
    user: TokenData = Depends(get_current_user),
):
    await announcement_service.delete_announcement(announcement_id, user.user_id)
    return Response(status_code=204)


@feed_router.patch("/{announcement_id}")
async def update_announcement(
    announcement_id: UUID,
    req: AnnouncementUpdateIn,
    announcement_service: AnnouncementListingService = Depends(
        get_announcement_listing_service
    ),
    user: TokenData = Depends(get_current_user),
):
    if announcement_id != req.announcement_id:
        raise HTTPException(status_code=400, detail="Invalid announcement ID")
    announcement = await announcement_service.update_announcement(req, user.user_id)

    return announcement
