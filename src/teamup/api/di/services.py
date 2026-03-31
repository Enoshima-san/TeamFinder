from sqlalchemy.ext.asyncio import AsyncSession

from teamup.application import (
    AddGameUseCase,
    AnnouncementListingService,
    AuthService,
    FullUserInfoUseCase,
    GamesService,
    GetUserGamesUseCase,
    ResponsesService,
)
from teamup.application.use_cases import GetUserUseCase

async def get_auth_service() -> AuthService:
    return AuthService()


async def get_announcement_listing_service() -> AnnouncementListingService:
    return AnnouncementListingService()
