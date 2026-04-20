from uuid import UUID

from fastapi import APIRouter, Depends, Response, status

from teamup.application.di import (
    get_announcement_service,
    get_games_service,
    get_user_use_case,
)
from teamup.application.services import AnnouncementService, GamesService
from teamup.application.use_cases import GetUserUseCase
from teamup.core import get_logger
from teamup.core.di import get_current_user
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
    ann_s: AnnouncementService = Depends(get_announcement_service),
):
    logger.info("Запрос на вывод всех активных объявлений.")
    res = await ann_s.get_active_announcements()
    return res


@feed_router.post(
    "/new", response_model=AnnouncementSummaryOut, status_code=status.HTTP_201_CREATED
)
async def create_announcement(
    req: AnnouncementCreateIn,
    token_data: TokenData = Depends(get_current_user),
    gu_uc: GetUserUseCase = Depends(get_user_use_case),
    game_s: GamesService = Depends(get_games_service),
    ann_s: AnnouncementService = Depends(get_announcement_service),
):
    announcement = await ann_s.create_announcement(req, token_data.user_id)
    user = await gu_uc(token_data.user_id)
    game = await game_s.get_game_by_id(req.game_id)

    res = AnnouncementSummaryOut.create(announcement, user, game)
    logger.info(
        f"Объявление {announcement.announcement_id} успешно создано пользователем {user.user_id}."
    )

    return res


@feed_router.get("/{announcement_id}", response_model=AnnouncementSummaryOut)
async def get_announcement(
    announcement_id: UUID,
    ann_s: AnnouncementService = Depends(get_announcement_service),
    token_data: TokenData = Depends(get_current_user),
):
    res = await ann_s.get_announcement_by_id(announcement_id)
    return res


@feed_router.delete("/{announcement_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_announcement(
    announcement_id: UUID,
    ann_s: AnnouncementService = Depends(get_announcement_service),
    token_data: TokenData = Depends(get_current_user),
):
    await ann_s.delete_announcement(announcement_id, token_data.user_id)
    return Response(status_code=204)


@feed_router.patch("/{announcement_id}", response_model=AnnouncementSummaryOut)
async def update_announcement(
    announcement_id: UUID,
    req: AnnouncementUpdateIn,
    ann_s: AnnouncementService = Depends(get_announcement_service),
    token_data: TokenData = Depends(get_current_user),
):
    res = await ann_s.update_announcement(req, announcement_id, token_data.user_id)
    return res
